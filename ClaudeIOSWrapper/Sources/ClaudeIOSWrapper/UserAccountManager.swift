import Foundation
import FirebaseAuth
import Combine

@MainActor
class UserAccountManager: ObservableObject {
    @Published var currentUser: User?
    @Published var isAuthenticated = false
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private var authStateListener: AuthStateDidChangeListenerHandle?
    
    init() {
        setupAuthStateListener()
    }
    
    deinit {
        if let listener = authStateListener {
            Auth.auth().removeStateDidChangeListener(listener)
        }
    }
    
    private func setupAuthStateListener() {
        authStateListener = Auth.auth().addStateDidChangeListener { [weak self] _, user in
            Task { @MainActor in
                self?.currentUser = user
                self?.isAuthenticated = user != nil
                
                if let user = user {
                    // Update last active timestamp
                    self?.updateUserLastActive(user)
                }
            }
        }
    }
    
    func checkAuthenticationState() {
        currentUser = Auth.auth().currentUser
        isAuthenticated = currentUser != nil
    }
    
    // MARK: - Authentication Methods
    
    func signIn(email: String, password: String) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let authResult = try await Auth.auth().signIn(withEmail: email, password: password)
            currentUser = authResult.user
            isAuthenticated = true
            
            // Log successful authentication
            await logActivity(.authentication, message: "User signed in successfully")
        } catch {
            errorMessage = error.localizedDescription
            await logActivity(.authentication, message: "Sign in failed: \(error.localizedDescription)")
        }
        
        isLoading = false
    }
    
    func signUp(email: String, password: String, displayName: String?) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let authResult = try await Auth.auth().createUser(withEmail: email, password: password)
            
            // Update display name if provided
            if let displayName = displayName, !displayName.isEmpty {
                let changeRequest = authResult.user.createProfileChangeRequest()
                changeRequest.displayName = displayName
                try await changeRequest.commitChanges()
            }
            
            currentUser = authResult.user
            isAuthenticated = true
            
            // Create user profile in Firestore
            await createUserProfile(authResult.user)
            
            // Log successful registration
            await logActivity(.authentication, message: "User registered successfully")
        } catch {
            errorMessage = error.localizedDescription
            await logActivity(.authentication, message: "Sign up failed: \(error.localizedDescription)")
        }
        
        isLoading = false
    }
    
    func signOut() {
        do {
            try Auth.auth().signOut()
            currentUser = nil
            isAuthenticated = false
            errorMessage = nil
            
            Task {
                await logActivity(.authentication, message: "User signed out")
            }
        } catch {
            errorMessage = error.localizedDescription
        }
    }
    
    func sendPasswordReset(email: String) async {
        isLoading = true
        errorMessage = nil
        
        do {
            try await Auth.auth().sendPasswordReset(withEmail: email)
            await logActivity(.authentication, message: "Password reset sent to \(email)")
        } catch {
            errorMessage = error.localizedDescription
            await logActivity(.authentication, message: "Password reset failed: \(error.localizedDescription)")
        }
        
        isLoading = false
    }
    
    func deleteAccount() async {
        guard let user = currentUser else { return }
        
        isLoading = true
        errorMessage = nil
        
        do {
            // Delete user data from Firestore first
            await deleteUserData(user.uid)
            
            // Delete Firebase Auth account
            try await user.delete()
            
            currentUser = nil
            isAuthenticated = false
            
            await logActivity(.authentication, message: "Account deleted")
        } catch {
            errorMessage = error.localizedDescription
            await logActivity(.authentication, message: "Account deletion failed: \(error.localizedDescription)")
        }
        
        isLoading = false
    }
    
    // MARK: - User Profile Management
    
    private func createUserProfile(_ user: User) async {
        let appUser = AppUser(from: user)
        
        // In a real app, you would save this to Firestore
        // For now, we'll just log it
        await logActivity(.authentication, message: "User profile created for \(user.email ?? "unknown")")
    }
    
    private func updateUserLastActive(_ user: User) {
        // In a real app, you would update this in Firestore
        // For now, we'll just log it
        Task {
            await logActivity(.authentication, message: "User last active updated")
        }
    }
    
    private func deleteUserData(_ userID: String) async {
        // In a real app, you would delete user data from Firestore
        // For now, we'll just log it
        await logActivity(.authentication, message: "User data deleted for \(userID)")
    }
    
    // MARK: - Validation
    
    func isValidEmail(_ email: String) -> Bool {
        let emailRegex = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}"
        let emailPredicate = NSPredicate(format:"SELF MATCHES %@", emailRegex)
        return emailPredicate.evaluate(with: email)
    }
    
    func isValidPassword(_ password: String) -> Bool {
        return password.count >= 6
    }
    
    // MARK: - Activity Logging
    
    private func logActivity(_ activityType: UserActivityLog.ActivityType, message: String, metadata: [String: String]? = nil) async {
        let log = UserActivityLog(
            userID: currentUser?.uid ?? "anonymous",
            activityType: activityType,
            message: message,
            timestamp: Date(),
            metadata: metadata
        )
        
        // In a real app, you would save this to Firestore or your logging service
        print("Activity Log: \(log.activityType.rawValue) - \(log.message)")
    }
    
    // MARK: - User Settings
    
    func getCurrentUserInfo() -> AppUser? {
        guard let firebaseUser = currentUser else { return nil }
        return AppUser(from: firebaseUser)
    }
    
    func updateProfile(displayName: String?) async {
        guard let user = currentUser else { return }
        
        isLoading = true
        errorMessage = nil
        
        do {
            let changeRequest = user.createProfileChangeRequest()
            changeRequest.displayName = displayName
            try await changeRequest.commitChanges()
            
            await logActivity(.authentication, message: "Profile updated")
        } catch {
            errorMessage = error.localizedDescription
            await logActivity(.authentication, message: "Profile update failed: \(error.localizedDescription)")
        }
        
        isLoading = false
    }
}
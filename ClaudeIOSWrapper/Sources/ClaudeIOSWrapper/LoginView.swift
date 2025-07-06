import SwiftUI

struct LoginView: View {
    @EnvironmentObject var userAccountManager: UserAccountManager
    @State private var email: String = ""
    @State private var password: String = ""
    @State private var confirmPassword: String = ""
    @State private var displayName: String = ""
    @State private var isSignUpMode: Bool = false
    @State private var showingPasswordReset: Bool = false
    @State private var resetEmail: String = ""
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // Header
                    headerView
                    
                    // Form
                    formView
                    
                    // Action Button
                    actionButton
                    
                    // Toggle Mode
                    toggleModeButton
                    
                    // Password Reset
                    if !isSignUpMode {
                        passwordResetButton
                    }
                    
                    // Error Message
                    if let errorMessage = userAccountManager.errorMessage {
                        errorView(errorMessage)
                    }
                }
                .padding(.horizontal, 32)
                .padding(.vertical, 40)
            }
            .background(
                LinearGradient(
                    gradient: Gradient(colors: [Color.blue.opacity(0.1), Color.purple.opacity(0.1)]),
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            )
            .navigationBarHidden(true)
        }
        .sheet(isPresented: $showingPasswordReset) {
            passwordResetSheet
        }
    }
    
    private var headerView: some View {
        VStack(spacing: 16) {
            // App Icon
            Image(systemName: "brain.head.profile")
                .font(.system(size: 64))
                .foregroundColor(.blue)
                .padding(.bottom, 8)
            
            Text("Claude Assistant")
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundColor(.primary)
            
            Text(isSignUpMode ? "Create your account" : "Welcome back")
                .font(.title3)
                .foregroundColor(.secondary)
        }
    }
    
    private var formView: some View {
        VStack(spacing: 16) {
            if isSignUpMode {
                CustomTextField(
                    title: "Display Name",
                    text: $displayName,
                    placeholder: "Enter your name",
                    systemImage: "person"
                )
            }
            
            CustomTextField(
                title: "Email",
                text: $email,
                placeholder: "Enter your email",
                systemImage: "envelope",
                keyboardType: .emailAddress
            )
            
            CustomSecureField(
                title: "Password",
                text: $password,
                placeholder: "Enter your password",
                systemImage: "lock"
            )
            
            if isSignUpMode {
                CustomSecureField(
                    title: "Confirm Password",
                    text: $confirmPassword,
                    placeholder: "Confirm your password",
                    systemImage: "lock.shield"
                )
            }
        }
    }
    
    private var actionButton: some View {
        Button(action: performAuthAction) {
            HStack {
                if userAccountManager.isLoading {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                        .scaleEffect(0.8)
                } else {
                    Text(isSignUpMode ? "Create Account" : "Sign In")
                        .fontWeight(.semibold)
                }
            }
            .frame(maxWidth: .infinity)
            .frame(height: 50)
            .background(
                isFormValid ? Color.blue : Color.gray
            )
            .foregroundColor(.white)
            .cornerRadius(12)
        }
        .disabled(!isFormValid || userAccountManager.isLoading)
    }
    
    private var toggleModeButton: some View {
        Button(action: {
            withAnimation(.easeInOut(duration: 0.3)) {
                isSignUpMode.toggle()
                clearForm()
            }
        }) {
            HStack {
                Text(isSignUpMode ? "Already have an account?" : "Don't have an account?")
                    .foregroundColor(.secondary)
                
                Text(isSignUpMode ? "Sign In" : "Sign Up")
                    .fontWeight(.semibold)
                    .foregroundColor(.blue)
            }
        }
    }
    
    private var passwordResetButton: some View {
        Button("Forgot Password?") {
            showingPasswordReset = true
        }
        .font(.footnote)
        .foregroundColor(.blue)
    }
    
    private func errorView(_ message: String) -> some View {
        HStack {
            Image(systemName: "exclamationmark.triangle.fill")
                .foregroundColor(.red)
            
            Text(message)
                .font(.caption)
                .foregroundColor(.red)
        }
        .padding()
        .background(Color.red.opacity(0.1))
        .cornerRadius(8)
    }
    
    private var passwordResetSheet: some View {
        NavigationView {
            VStack(spacing: 24) {
                Text("Reset Password")
                    .font(.title2)
                    .fontWeight(.bold)
                
                Text("Enter your email address and we'll send you a link to reset your password.")
                    .font(.body)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                
                CustomTextField(
                    title: "Email",
                    text: $resetEmail,
                    placeholder: "Enter your email",
                    systemImage: "envelope",
                    keyboardType: .emailAddress
                )
                
                Button(action: sendPasswordReset) {
                    Text("Send Reset Link")
                        .fontWeight(.semibold)
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(userAccountManager.isValidEmail(resetEmail) ? Color.blue : Color.gray)
                        .foregroundColor(.white)
                        .cornerRadius(12)
                }
                .disabled(!userAccountManager.isValidEmail(resetEmail) || userAccountManager.isLoading)
                
                Spacer()
            }
            .padding()
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        showingPasswordReset = false
                        resetEmail = ""
                    }
                }
            }
        }
        .presentationDetents([.medium])
    }
    
    // MARK: - Computed Properties
    
    private var isFormValid: Bool {
        let emailValid = userAccountManager.isValidEmail(email)
        let passwordValid = userAccountManager.isValidPassword(password)
        
        if isSignUpMode {
            let passwordsMatch = password == confirmPassword
            return emailValid && passwordValid && passwordsMatch && !displayName.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
        } else {
            return emailValid && passwordValid
        }
    }
    
    // MARK: - Actions
    
    private func performAuthAction() {
        Task {
            if isSignUpMode {
                await userAccountManager.signUp(
                    email: email,
                    password: password,
                    displayName: displayName.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty ? nil : displayName
                )
            } else {
                await userAccountManager.signIn(email: email, password: password)
            }
        }
    }
    
    private func sendPasswordReset() {
        Task {
            await userAccountManager.sendPasswordReset(email: resetEmail)
            showingPasswordReset = false
            resetEmail = ""
        }
    }
    
    private func clearForm() {
        email = ""
        password = ""
        confirmPassword = ""
        displayName = ""
        userAccountManager.errorMessage = nil
    }
}

// MARK: - Custom UI Components

struct CustomTextField: View {
    let title: String
    @Binding var text: String
    let placeholder: String
    let systemImage: String
    var keyboardType: UIKeyboardType = .default
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.headline)
                .foregroundColor(.primary)
            
            HStack {
                Image(systemName: systemImage)
                    .foregroundColor(.secondary)
                    .frame(width: 20)
                
                TextField(placeholder, text: $text)
                    .keyboardType(keyboardType)
                    .autocapitalization(.none)
                    .disableAutocorrection(true)
            }
            .padding()
            .background(Color(.systemGray6))
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.blue.opacity(0.3), lineWidth: 1)
            )
        }
    }
}

struct CustomSecureField: View {
    let title: String
    @Binding var text: String
    let placeholder: String
    let systemImage: String
    @State private var isSecure = true
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.headline)
                .foregroundColor(.primary)
            
            HStack {
                Image(systemName: systemImage)
                    .foregroundColor(.secondary)
                    .frame(width: 20)
                
                if isSecure {
                    SecureField(placeholder, text: $text)
                } else {
                    TextField(placeholder, text: $text)
                        .autocapitalization(.none)
                        .disableAutocorrection(true)
                }
                
                Button(action: {
                    isSecure.toggle()
                }) {
                    Image(systemName: isSecure ? "eye.slash" : "eye")
                        .foregroundColor(.secondary)
                }
            }
            .padding()
            .background(Color(.systemGray6))
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.blue.opacity(0.3), lineWidth: 1)
            )
        }
    }
}

#Preview {
    LoginView()
        .environmentObject(UserAccountManager())
}
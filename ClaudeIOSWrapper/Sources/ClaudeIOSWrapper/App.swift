import SwiftUI
import Firebase

@main
struct ClaudeIOSWrapperApp: App {
    @StateObject private var userAccountManager = UserAccountManager()
    @StateObject private var claudeAPIService = ClaudeAPIService()
    @StateObject private var loggingService = LoggingService()
    
    init() {
        FirebaseApp.configure()
    }
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(userAccountManager)
                .environmentObject(claudeAPIService)
                .environmentObject(loggingService)
                .onAppear {
                    userAccountManager.checkAuthenticationState()
                }
        }
    }
}
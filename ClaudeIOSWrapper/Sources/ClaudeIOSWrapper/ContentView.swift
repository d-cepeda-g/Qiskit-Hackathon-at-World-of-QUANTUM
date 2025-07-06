import SwiftUI

struct ContentView: View {
    @EnvironmentObject var userAccountManager: UserAccountManager
    @EnvironmentObject var claudeAPIService: ClaudeAPIService
    @EnvironmentObject var loggingService: LoggingService
    @State private var messageText: String = ""
    @State private var isLoading: Bool = false
    
    var body: some View {
        NavigationView {
            if userAccountManager.isAuthenticated {
                VStack(spacing: 0) {
                    // Header
                    headerView
                    
                    // Chat Messages
                    ScrollView {
                        LazyVStack(alignment: .leading, spacing: 12) {
                            ForEach(claudeAPIService.messages) { message in
                                MessageBubbleView(message: message)
                            }
                        }
                        .padding()
                    }
                    .background(Color(.systemGray6))
                    
                    // Input Area
                    inputView
                }
                .navigationBarHidden(true)
            } else {
                LoginView()
            }
        }
    }
    
    private var headerView: some View {
        HStack {
            VStack(alignment: .leading) {
                Text("Claude Assistant")
                    .font(.title2)
                    .fontWeight(.bold)
                Text("AI-Powered Conversations")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            Button(action: {
                userAccountManager.signOut()
            }) {
                Image(systemName: "person.circle")
                    .font(.title2)
                    .foregroundColor(.blue)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .shadow(radius: 1)
    }
    
    private var inputView: some View {
        VStack {
            HStack {
                TextField("Type your message...", text: $messageText, axis: .vertical)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .lineLimit(1...4)
                
                Button(action: sendMessage) {
                    Image(systemName: isLoading ? "stop.circle" : "arrow.up.circle.fill")
                        .font(.title2)
                        .foregroundColor(messageText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty ? .gray : .blue)
                }
                .disabled(messageText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty && !isLoading)
            }
            .padding()
        }
        .background(Color(.systemBackground))
    }
    
    private func sendMessage() {
        guard !messageText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { return }
        
        if isLoading {
            claudeAPIService.cancelCurrentRequest()
            isLoading = false
            return
        }
        
        let userMessage = messageText
        messageText = ""
        isLoading = true
        
        // Log the user interaction
        loggingService.logUserMessage(userMessage, userID: userAccountManager.currentUser?.uid ?? "unknown")
        
        Task {
            do {
                let response = try await claudeAPIService.sendMessage(userMessage)
                loggingService.logClaudeResponse(response, userID: userAccountManager.currentUser?.uid ?? "unknown")
                isLoading = false
            } catch {
                loggingService.logError(error, userID: userAccountManager.currentUser?.uid ?? "unknown")
                isLoading = false
            }
        }
    }
}
import Foundation
import Alamofire
import Combine

@MainActor
class ClaudeAPIService: ObservableObject {
    @Published var messages: [ChatMessage] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private var currentRequest: DataRequest?
    private let apiKey: String
    
    init() {
        // In a real app, this should be securely stored in Keychain or loaded from a secure configuration
        self.apiKey = ProcessInfo.processInfo.environment["CLAUDE_API_KEY"] ?? ""
        if apiKey.isEmpty {
            print("Warning: CLAUDE_API_KEY environment variable not set")
        }
    }
    
    func sendMessage(_ userMessage: String) async throws -> String {
        let userChatMessage = ChatMessage(content: userMessage, isUser: true)
        messages.append(userChatMessage)
        
        isLoading = true
        errorMessage = nil
        
        do {
            let response = try await callClaudeAPI(with: userMessage)
            let claudeResponse = response.content.first?.text ?? "No response"
            
            let claudeChatMessage = ChatMessage(content: claudeResponse, isUser: false, messageID: response.id)
            messages.append(claudeChatMessage)
            
            isLoading = false
            return claudeResponse
        } catch {
            isLoading = false
            errorMessage = error.localizedDescription
            throw error
        }
    }
    
    func cancelCurrentRequest() {
        currentRequest?.cancel()
        currentRequest = nil
        isLoading = false
    }
    
    private func callClaudeAPI(with message: String) async throws -> ClaudeAPIResponse {
        guard !apiKey.isEmpty else {
            throw ClaudeAPIError.invalidAPIKey
        }
        
        let conversationMessages = buildConversationHistory(with: message)
        
        let request = ClaudeAPIRequest(
            model: APIConfiguration.defaultModel,
            maxTokens: APIConfiguration.maxTokens,
            messages: conversationMessages,
            system: APIConfiguration.systemPrompt
        )
        
        let headers: HTTPHeaders = [
            "Content-Type": "application/json",
            "x-api-key": apiKey,
            "anthropic-version": "2023-06-01"
        ]
        
        return try await withCheckedThrowingContinuation { continuation in
            currentRequest = AF.request(
                APIConfiguration.claudeAPIURL,
                method: .post,
                parameters: request,
                encoder: JSONParameterEncoder.default,
                headers: headers
            )
            .validate()
            .responseDecodable(of: ClaudeAPIResponse.self) { response in
                switch response.result {
                case .success(let claudeResponse):
                    continuation.resume(returning: claudeResponse)
                case .failure(let error):
                    let claudeError = self.mapAlamofireError(error, statusCode: response.response?.statusCode)
                    continuation.resume(throwing: claudeError)
                }
            }
        }
    }
    
    private func buildConversationHistory(with newMessage: String) -> [ClaudeMessage] {
        var conversationMessages: [ClaudeMessage] = []
        
        // Add previous messages (limit to last 10 exchanges to manage token usage)
        let recentMessages = messages.suffix(20) // Last 10 user + 10 assistant messages
        
        for chatMessage in recentMessages {
            let role = chatMessage.isUser ? "user" : "assistant"
            conversationMessages.append(ClaudeMessage(role: role, content: chatMessage.content))
        }
        
        // Add the new user message
        conversationMessages.append(ClaudeMessage(role: "user", content: newMessage))
        
        return conversationMessages
    }
    
    private func mapAlamofireError(_ error: AFError, statusCode: Int?) -> ClaudeAPIError {
        if let statusCode = statusCode {
            switch statusCode {
            case 401:
                return .invalidAPIKey
            case 429:
                return .rateLimitExceeded
            case 500...599:
                return .serverError(statusCode)
            default:
                return .networkError("HTTP \(statusCode): \(error.localizedDescription)")
            }
        }
        
        if error.isConnectivityError {
            return .networkError("No internet connection")
        }
        
        return .unknown(error.localizedDescription)
    }
    
    func clearConversation() {
        messages.removeAll()
        errorMessage = nil
    }
    
    func exportConversation() -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        
        var export = "Claude Conversation Export\n"
        export += "Generated: \(formatter.string(from: Date()))\n\n"
        
        for message in messages {
            let sender = message.isUser ? "User" : "Claude"
            let timestamp = formatter.string(from: message.timestamp)
            export += "[\(timestamp)] \(sender):\n\(message.content)\n\n"
        }
        
        return export
    }
}
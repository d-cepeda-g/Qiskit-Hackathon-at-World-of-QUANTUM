import Foundation
import FirebaseAuth

// MARK: - Message Models
struct ChatMessage: Identifiable, Codable {
    let id = UUID()
    let content: String
    let isUser: Bool
    let timestamp: Date
    let messageID: String?
    
    init(content: String, isUser: Bool, messageID: String? = nil) {
        self.content = content
        self.isUser = isUser
        self.timestamp = Date()
        self.messageID = messageID
    }
}

// MARK: - Claude API Models
struct ClaudeAPIRequest: Codable {
    let model: String
    let maxTokens: Int
    let messages: [ClaudeMessage]
    let system: String?
    
    enum CodingKeys: String, CodingKey {
        case model
        case maxTokens = "max_tokens"
        case messages
        case system
    }
}

struct ClaudeMessage: Codable {
    let role: String
    let content: String
}

struct ClaudeAPIResponse: Codable {
    let id: String
    let type: String
    let role: String
    let content: [ClaudeContent]
    let model: String
    let stopReason: String?
    let stopSequence: String?
    let usage: ClaudeUsage
    
    enum CodingKeys: String, CodingKey {
        case id, type, role, content, model
        case stopReason = "stop_reason"
        case stopSequence = "stop_sequence"
        case usage
    }
}

struct ClaudeContent: Codable {
    let type: String
    let text: String
}

struct ClaudeUsage: Codable {
    let inputTokens: Int
    let outputTokens: Int
    
    enum CodingKeys: String, CodingKey {
        case inputTokens = "input_tokens"
        case outputTokens = "output_tokens"
    }
}

// MARK: - User Models
struct AppUser: Codable {
    let uid: String
    let email: String
    let displayName: String?
    let createdAt: Date
    let lastActiveAt: Date
    
    init(from firebaseUser: User) {
        self.uid = firebaseUser.uid
        self.email = firebaseUser.email ?? ""
        self.displayName = firebaseUser.displayName
        self.createdAt = firebaseUser.metadata.creationDate ?? Date()
        self.lastActiveAt = firebaseUser.metadata.lastSignInDate ?? Date()
    }
}

// MARK: - Logging Models
struct UserActivityLog: Codable {
    let id = UUID()
    let userID: String
    let activityType: ActivityType
    let message: String
    let timestamp: Date
    let metadata: [String: String]?
    
    enum ActivityType: String, Codable, CaseIterable {
        case userMessage = "user_message"
        case claudeResponse = "claude_response"
        case apiError = "api_error"
        case authentication = "authentication"
        case appLaunch = "app_launch"
        case appBackground = "app_background"
    }
}

// MARK: - API Configuration
struct APIConfiguration {
    static let claudeAPIURL = "https://api.anthropic.com/v1/messages"
    static let defaultModel = "claude-3-5-sonnet-20241022"
    static let maxTokens = 4096
    static let systemPrompt = "You are Claude, an AI assistant created by Anthropic. You are helpful, harmless, and honest."
}

// MARK: - Error Models
enum ClaudeAPIError: Error, LocalizedError {
    case invalidAPIKey
    case networkError(String)
    case decodingError(String)
    case rateLimitExceeded
    case serverError(Int)
    case unknown(String)
    
    var errorDescription: String? {
        switch self {
        case .invalidAPIKey:
            return "Invalid API key. Please check your Claude API credentials."
        case .networkError(let message):
            return "Network error: \(message)"
        case .decodingError(let message):
            return "Failed to decode response: \(message)"
        case .rateLimitExceeded:
            return "Rate limit exceeded. Please try again later."
        case .serverError(let code):
            return "Server error with code: \(code)"
        case .unknown(let message):
            return "Unknown error: \(message)"
        }
    }
}
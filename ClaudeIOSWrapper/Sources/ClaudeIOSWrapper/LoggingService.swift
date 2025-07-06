import Foundation
import FirebaseFirestore
import Combine

@MainActor
class LoggingService: ObservableObject {
    @Published var logs: [UserActivityLog] = []
    @Published var isLoading = false
    
    private let db = Firestore.firestore()
    private let maxLocalLogs = 1000 // Maximum number of logs to keep locally
    
    init() {
        startSession()
    }
    
    // MARK: - Session Management
    
    func startSession() {
        logActivity(.appLaunch, message: "App launched", userID: "system")
    }
    
    func endSession() {
        logActivity(.appBackground, message: "App backgrounded", userID: "system")
        uploadPendingLogs()
    }
    
    // MARK: - Logging Methods
    
    func logUserMessage(_ message: String, userID: String) {
        let metadata = [
            "message_length": "\(message.count)",
            "message_type": "user_input"
        ]
        
        logActivity(.userMessage, message: "User sent message", userID: userID, metadata: metadata)
    }
    
    func logClaudeResponse(_ response: String, userID: String) {
        let metadata = [
            "response_length": "\(response.count)",
            "message_type": "claude_response"
        ]
        
        logActivity(.claudeResponse, message: "Claude responded", userID: userID, metadata: metadata)
    }
    
    func logError(_ error: Error, userID: String) {
        let metadata = [
            "error_type": "\(type(of: error))",
            "error_domain": (error as NSError).domain,
            "error_code": "\((error as NSError).code)"
        ]
        
        logActivity(.apiError, message: error.localizedDescription, userID: userID, metadata: metadata)
    }
    
    func logActivity(_ activityType: UserActivityLog.ActivityType, message: String, userID: String, metadata: [String: String]? = nil) {
        let log = UserActivityLog(
            userID: userID,
            activityType: activityType,
            message: message,
            timestamp: Date(),
            metadata: metadata
        )
        
        // Add to local storage
        logs.append(log)
        
        // Maintain local log limit
        if logs.count > maxLocalLogs {
            logs.removeFirst(logs.count - maxLocalLogs)
        }
        
        // Upload to Firestore (async)
        Task {
            await uploadLog(log)
        }
        
        // Print for debugging
        print("📊 Log: [\(activityType.rawValue)] \(message)")
        if let metadata = metadata {
            print("   Metadata: \(metadata)")
        }
    }
    
    // MARK: - Cloud Storage
    
    private func uploadLog(_ log: UserActivityLog) async {
        do {
            let logData = try Firestore.Encoder().encode(log)
            try await db.collection("user_logs").document(log.id.uuidString).setData(logData)
        } catch {
            print("Failed to upload log: \(error.localizedDescription)")
            // In a production app, you might want to queue failed uploads for retry
        }
    }
    
    private func uploadPendingLogs() {
        // In a production app, you would implement a queue system for failed uploads
        Task {
            for log in logs.suffix(10) { // Upload last 10 logs on app background
                await uploadLog(log)
            }
        }
    }
    
    // MARK: - Analytics and Reporting
    
    func getUserActivitySummary(userID: String) -> ActivitySummary {
        let userLogs = logs.filter { $0.userID == userID }
        
        let messageCount = userLogs.filter { $0.activityType == .userMessage }.count
        let responseCount = userLogs.filter { $0.activityType == .claudeResponse }.count
        let errorCount = userLogs.filter { $0.activityType == .apiError }.count
        
        let sessionStart = userLogs.first?.timestamp ?? Date()
        let sessionDuration = Date().timeIntervalSince(sessionStart)
        
        return ActivitySummary(
            userID: userID,
            messageCount: messageCount,
            responseCount: responseCount,
            errorCount: errorCount,
            sessionDuration: sessionDuration,
            lastActivity: userLogs.last?.timestamp ?? Date()
        )
    }
    
    func getLogsForDateRange(start: Date, end: Date) -> [UserActivityLog] {
        return logs.filter { log in
            log.timestamp >= start && log.timestamp <= end
        }
    }
    
    func getLogsForUser(_ userID: String) -> [UserActivityLog] {
        return logs.filter { $0.userID == userID }
    }
    
    func getErrorLogs() -> [UserActivityLog] {
        return logs.filter { $0.activityType == .apiError }
    }
    
    // MARK: - Export and Sharing
    
    func exportLogsAsJSON() throws -> Data {
        return try JSONEncoder().encode(logs)
    }
    
    func exportLogsAsCSV() -> String {
        var csv = "Timestamp,UserID,ActivityType,Message,Metadata\n"
        
        for log in logs {
            let timestamp = ISO8601DateFormatter().string(from: log.timestamp)
            let metadata = log.metadata?.map { "\($0.key):\($0.value)" }.joined(separator: ";") ?? ""
            let escapedMessage = log.message.replacingOccurrences(of: "\"", with: "\"\"")
            
            csv += "\"\(timestamp)\",\"\(log.userID)\",\"\(log.activityType.rawValue)\",\"\(escapedMessage)\",\"\(metadata)\"\n"
        }
        
        return csv
    }
    
    // MARK: - Privacy and Data Management
    
    func clearUserLogs(userID: String) {
        logs.removeAll { $0.userID == userID }
        
        // Also delete from Firestore
        Task {
            await deleteUserLogsFromFirestore(userID: userID)
        }
    }
    
    func clearAllLogs() {
        logs.removeAll()
        
        // Clear from Firestore (be careful with this in production!)
        Task {
            await deleteAllLogsFromFirestore()
        }
    }
    
    private func deleteUserLogsFromFirestore(userID: String) async {
        do {
            let query = db.collection("user_logs").whereField("userID", isEqualTo: userID)
            let snapshot = try await query.getDocuments()
            
            for document in snapshot.documents {
                try await document.reference.delete()
            }
        } catch {
            print("Failed to delete user logs from Firestore: \(error.localizedDescription)")
        }
    }
    
    private func deleteAllLogsFromFirestore() async {
        do {
            let snapshot = try await db.collection("user_logs").getDocuments()
            
            for document in snapshot.documents {
                try await document.reference.delete()
            }
        } catch {
            print("Failed to delete all logs from Firestore: \(error.localizedDescription)")
        }
    }
    
    // MARK: - Performance Monitoring
    
    func trackPerformanceMetric(name: String, value: Double, userID: String) {
        let metadata = [
            "metric_name": name,
            "metric_value": "\(value)",
            "metric_type": "performance"
        ]
        
        logActivity(.userMessage, message: "Performance metric: \(name) = \(value)", userID: userID, metadata: metadata)
    }
}

// MARK: - Supporting Models

struct ActivitySummary {
    let userID: String
    let messageCount: Int
    let responseCount: Int
    let errorCount: Int
    let sessionDuration: TimeInterval
    let lastActivity: Date
    
    var averageResponseTime: TimeInterval? {
        guard responseCount > 0 else { return nil }
        return sessionDuration / Double(responseCount)
    }
    
    var errorRate: Double {
        let totalActions = messageCount + responseCount
        guard totalActions > 0 else { return 0 }
        return Double(errorCount) / Double(totalActions)
    }
}
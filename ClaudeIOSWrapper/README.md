# Claude iOS Wrapper

A modern iOS application that provides a beautiful interface for interacting with Claude AI, complete with user authentication and comprehensive logging functionality.

## Features

### 🤖 Claude AI Integration
- Full integration with Claude API (Anthropic)
- Support for Claude 3.5 Sonnet model
- Real-time conversation with contextual memory
- Message history and conversation export
- Error handling and retry mechanisms

### 🔐 User Authentication
- Firebase Authentication integration
- Email/password sign up and sign in
- Password reset functionality
- User profile management
- Session persistence

### 📊 Comprehensive Logging
- Real-time activity tracking
- Firestore cloud storage for logs
- User interaction analytics
- Error logging and monitoring
- Export capabilities (JSON/CSV)
- Privacy-compliant data management

### 🎨 Modern UI/UX
- Native SwiftUI interface
- Dark/Light mode support
- Responsive design for iPhone and iPad
- Smooth animations and transitions
- Typing indicators and message bubbles
- Pull-to-refresh and real-time updates

## Prerequisites

- Xcode 15.0 or later
- iOS 15.0 or later
- Swift 5.9 or later
- Claude API key from Anthropic
- Firebase project with Authentication and Firestore enabled

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd ClaudeIOSWrapper
```

### 2. Firebase Configuration

1. Create a new Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Authentication (Email/Password provider)
3. Enable Firestore Database
4. Download `GoogleService-Info.plist` and add it to your Xcode project
5. Copy the provided template and configure with your Firebase settings

### 3. Claude API Setup

1. Get your Claude API key from [Anthropic Console](https://console.anthropic.com/)
2. Set the environment variable:
   ```bash
   export CLAUDE_API_KEY="your-api-key-here"
   ```
3. Or add it to your app's environment variables in Xcode

### 4. Xcode Project Setup

1. Open `ClaudeIOSWrapper.xcworkspace` in Xcode
2. Add your team and bundle identifier
3. Ensure all dependencies are resolved
4. Add `GoogleService-Info.plist` to the project target
5. Configure signing & capabilities

### 5. Run the App

1. Select your target device/simulator
2. Build and run the project (⌘+R)

## Configuration

### Environment Variables

Create a `.env` file in your project root:

```env
CLAUDE_API_KEY=your_claude_api_key_here
FIREBASE_PROJECT_ID=your_firebase_project_id
APP_BUNDLE_ID=com.yourcompany.claudewrapper
```

### Firebase Rules

Configure Firestore security rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only access their own logs
    match /user_logs/{logId} {
      allow read, write: if request.auth != null && 
        request.auth.uid == resource.data.userID;
    }
    
    // User profiles
    match /users/{userId} {
      allow read, write: if request.auth != null && 
        request.auth.uid == userId;
    }
  }
}
```

## Usage

### Basic Chat
1. Sign up or sign in with your email
2. Start typing your message to Claude
3. Send messages and receive AI responses
4. View conversation history

### Account Management
- Update profile information
- Reset password
- Sign out securely
- Delete account (with data removal)

### Logging Features
- All interactions are automatically logged
- View activity summaries
- Export conversation history
- Monitor API usage and errors

## API Reference

### ClaudeAPIService

```swift
// Send a message to Claude
func sendMessage(_ userMessage: String) async throws -> String

// Cancel current request
func cancelCurrentRequest()

// Clear conversation history
func clearConversation()

// Export conversation
func exportConversation() -> String
```

### UserAccountManager

```swift
// Authentication
func signIn(email: String, password: String) async
func signUp(email: String, password: String, displayName: String?) async
func signOut()

// Profile management
func updateProfile(displayName: String?) async
func sendPasswordReset(email: String) async
```

### LoggingService

```swift
// Activity logging
func logUserMessage(_ message: String, userID: String)
func logClaudeResponse(_ response: String, userID: String)
func logError(_ error: Error, userID: String)

// Analytics
func getUserActivitySummary(userID: String) -> ActivitySummary
func exportLogsAsJSON() throws -> Data
func exportLogsAsCSV() -> String
```

## Architecture

### MVVM Pattern
- **Models**: `ChatMessage`, `AppUser`, `UserActivityLog`
- **Views**: SwiftUI views with modern design
- **ViewModels**: Observable objects with Combine framework

### Services
- **ClaudeAPIService**: Handles all Claude API communication
- **UserAccountManager**: Manages Firebase authentication
- **LoggingService**: Comprehensive activity tracking

### Data Flow
1. User input → ContentView
2. ContentView → ClaudeAPIService
3. API response → UI update + LoggingService
4. Logs → Firestore storage

## Security

### Data Protection
- API keys stored securely
- User data encrypted in transit and at rest
- Firebase security rules enforced
- Privacy-compliant logging

### Best Practices
- No sensitive data in logs
- User consent for data collection
- GDPR/CCPA compliance ready
- Secure key management

## Customization

### Themes
Modify colors and styles in:
- `ContentView.swift` - Main chat interface
- `LoginView.swift` - Authentication screens
- `MessageBubbleView.swift` - Chat bubbles

### API Configuration
Update settings in `Models.swift`:
```swift
struct APIConfiguration {
    static let claudeAPIURL = "https://api.anthropic.com/v1/messages"
    static let defaultModel = "claude-3-5-sonnet-20241022"
    static let maxTokens = 4096
}
```

## Troubleshooting

### Common Issues

**API Key Issues**
- Ensure `CLAUDE_API_KEY` environment variable is set
- Verify API key is valid and has sufficient credits
- Check network connectivity

**Firebase Issues**
- Verify `GoogleService-Info.plist` is included in project
- Ensure Firebase project has Authentication and Firestore enabled
- Check Firebase security rules

**Build Errors**
- Clean build folder (⌘+Shift+K)
- Reset package caches
- Verify all dependencies are resolved

### Debug Mode
Enable debug logging by setting:
```swift
// In App.swift
#if DEBUG
print("Debug mode enabled")
#endif
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review Firebase and Anthropic documentation

## Roadmap

### Upcoming Features
- [ ] Voice message support
- [ ] Image analysis with Claude
- [ ] Conversation templates
- [ ] Advanced export options
- [ ] Multi-language support
- [ ] Dark mode customization
- [ ] Widget support
- [ ] Apple Watch companion app

### Technical Improvements
- [ ] Offline message queuing
- [ ] Advanced caching
- [ ] Performance optimizations
- [ ] Unit and UI tests
- [ ] CI/CD pipeline
- [ ] App Store deployment

---

**Note**: This is a demonstration project. For production use, implement additional security measures, error handling, and testing as appropriate for your use case.
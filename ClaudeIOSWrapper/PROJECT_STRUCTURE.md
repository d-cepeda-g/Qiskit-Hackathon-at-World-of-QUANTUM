# Claude iOS Wrapper - Project Structure

This document provides an overview of the project structure and explains the purpose of each file and directory.

## Project Overview

```
ClaudeIOSWrapper/
├── Package.swift                           # Swift Package Manager configuration
├── Sources/ClaudeIOSWrapper/              # Main source code directory
│   ├── App.swift                          # Main app entry point
│   ├── ContentView.swift                  # Main chat interface
│   ├── LoginView.swift                    # Authentication UI
│   ├── MessageBubbleView.swift            # Chat message components
│   ├── Models.swift                       # Data models and structures
│   ├── ClaudeAPIService.swift             # Claude API integration
│   ├── UserAccountManager.swift           # Firebase authentication
│   └── LoggingService.swift               # Activity logging and analytics
├── Info.plist                             # iOS app configuration
├── GoogleService-Info.plist.template      # Firebase configuration template
├── .env.example                           # Environment variables template
├── .gitignore                             # Git ignore rules
├── README.md                              # Main documentation
└── PROJECT_STRUCTURE.md                  # This file
```

## Core Files

### `Package.swift`
- **Purpose**: Swift Package Manager configuration
- **Contains**: Dependencies (Alamofire, Firebase, Swift Crypto)
- **Target Platform**: iOS 15.0+
- **Key Dependencies**:
  - Alamofire for HTTP networking
  - Firebase SDK for authentication and database
  - Swift Crypto for security operations

### `App.swift`
- **Purpose**: Main application entry point
- **Contains**: App lifecycle management and dependency injection
- **Key Features**:
  - Firebase initialization
  - Environment object setup
  - Authentication state monitoring

## UI Components

### `ContentView.swift`
- **Purpose**: Main chat interface and navigation controller
- **Contains**: Chat UI, message input, user authentication state handling
- **Key Features**:
  - Real-time message display
  - Input handling and validation
  - Loading states and error handling
  - Navigation between authenticated/unauthenticated states

### `LoginView.swift`
- **Purpose**: User authentication interface
- **Contains**: Sign in, sign up, password reset functionality
- **Key Features**:
  - Email/password authentication
  - Form validation
  - Custom UI components (CustomTextField, CustomSecureField)
  - Password reset modal
  - Modern gradient background

### `MessageBubbleView.swift`
- **Purpose**: Chat message display components
- **Contains**: Message bubbles, typing indicators, action buttons
- **Key Features**:
  - User vs Claude message styling
  - Timestamp formatting
  - Message actions (copy, share, expand)
  - Typing animation
  - Bubble tails and avatars

## Data and Models

### `Models.swift`
- **Purpose**: Data structures and type definitions
- **Contains**: All app data models and configuration
- **Key Components**:
  - `ChatMessage`: Individual message structure
  - `ClaudeAPIRequest/Response`: API communication models
  - `AppUser`: User profile data
  - `UserActivityLog`: Logging data structure
  - `APIConfiguration`: API settings and endpoints
  - `ClaudeAPIError`: Error handling types

## Services

### `ClaudeAPIService.swift`
- **Purpose**: Claude API integration and communication
- **Contains**: HTTP requests, response handling, conversation management
- **Key Features**:
  - Async/await API calls
  - Request cancellation
  - Error mapping and handling
  - Conversation history management
  - Token usage optimization
  - Export functionality

### `UserAccountManager.swift`
- **Purpose**: User authentication and profile management
- **Contains**: Firebase Auth integration, user state management
- **Key Features**:
  - Email/password authentication
  - Profile management
  - Password reset
  - Account deletion
  - Session persistence
  - Activity logging integration

### `LoggingService.swift`
- **Purpose**: Activity tracking and analytics
- **Contains**: Event logging, data storage, export capabilities
- **Key Features**:
  - Real-time activity logging
  - Firestore cloud storage
  - Local log management
  - Export to JSON/CSV
  - Privacy compliance
  - Performance monitoring

## Configuration Files

### `Info.plist`
- **Purpose**: iOS app configuration and permissions
- **Contains**: App metadata, permissions, security settings
- **Key Settings**:
  - Network security configuration
  - Privacy usage descriptions
  - Background modes
  - Document types
  - URL schemes

### `GoogleService-Info.plist.template`
- **Purpose**: Firebase configuration template
- **Contains**: Placeholder Firebase project settings
- **Usage**: Replace with actual Firebase configuration file
- **Security**: Never commit actual file to version control

### `.env.example`
- **Purpose**: Environment variables template
- **Contains**: Configuration options and API keys template
- **Usage**: Copy to `.env` and fill with actual values
- **Categories**:
  - API keys and endpoints
  - Feature flags
  - Performance settings
  - Security options

### `.gitignore`
- **Purpose**: Version control exclusion rules
- **Contains**: Files and directories to exclude from Git
- **Protects**:
  - API keys and secrets
  - Build artifacts
  - User-specific settings
  - Generated files

## Architecture Patterns

### MVVM (Model-View-ViewModel)
- **Models**: Data structures in `Models.swift`
- **Views**: SwiftUI components (`ContentView`, `LoginView`, etc.)
- **ViewModels**: Observable objects (`ClaudeAPIService`, `UserAccountManager`, `LoggingService`)

### Service Layer Pattern
- **ClaudeAPIService**: External API communication
- **UserAccountManager**: Authentication and user management
- **LoggingService**: Data tracking and analytics

### Dependency Injection
- Environment objects passed through SwiftUI view hierarchy
- Centralized service management
- Testable architecture

## Data Flow

### Authentication Flow
1. `App.swift` → `UserAccountManager` → Firebase Auth
2. Authentication state → `ContentView` navigation
3. User actions → `LoginView` → `UserAccountManager`

### Chat Flow
1. User input → `ContentView` → `ClaudeAPIService`
2. API response → UI update + `LoggingService`
3. Message storage → local array + Firestore logs

### Logging Flow
1. User action → Service layer → `LoggingService`
2. Local storage + Firestore upload
3. Analytics and export capabilities

## Security Considerations

### API Key Management
- Environment variables for development
- Secure storage recommendations
- No hardcoded keys in source

### User Data Protection
- Firebase security rules
- Encrypted data transmission
- Privacy-compliant logging

### Authentication Security
- Firebase Auth best practices
- Session management
- Password validation

## Extensibility Points

### New Features
- Add new services in service layer
- Extend models for new data types
- Create new UI components

### Customization
- Theme customization in UI components
- API configuration in `Models.swift`
- Feature flags in environment variables

### Testing
- Service layer is unit testable
- UI components support SwiftUI previews
- Dependency injection enables mocking

## Development Workflow

### Initial Setup
1. Clone repository
2. Install dependencies
3. Configure Firebase
4. Set environment variables
5. Build and run

### Making Changes
1. Modify appropriate service or view
2. Update models if needed
3. Test in simulator
4. Update documentation

### Deployment
1. Configure production environment
2. Set production API keys
3. Build for release
4. Submit to App Store

---

This structure provides a solid foundation for a production-ready iOS application with modern architecture patterns, comprehensive logging, and secure user management.
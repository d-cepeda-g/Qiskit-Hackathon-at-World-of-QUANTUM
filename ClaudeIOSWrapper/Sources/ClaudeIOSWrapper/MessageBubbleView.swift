import SwiftUI

struct MessageBubbleView: View {
    let message: ChatMessage
    
    var body: some View {
        HStack {
            if message.isUser {
                Spacer(minLength: 50)
                messageContent
            } else {
                messageContent
                Spacer(minLength: 50)
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 4)
    }
    
    private var messageContent: some View {
        VStack(alignment: message.isUser ? .trailing : .leading, spacing: 4) {
            HStack {
                if !message.isUser {
                    avatarView
                }
                
                VStack(alignment: message.isUser ? .trailing : .leading, spacing: 4) {
                    messageBubble
                    timestampView
                }
                
                if message.isUser {
                    avatarView
                }
            }
        }
    }
    
    private var avatarView: some View {
        Circle()
            .fill(message.isUser ? Color.blue : Color.orange)
            .frame(width: 32, height: 32)
            .overlay(
                Image(systemName: message.isUser ? "person.fill" : "brain.head.profile")
                    .font(.system(size: 16, weight: .medium))
                    .foregroundColor(.white)
            )
    }
    
    private var messageBubble: some View {
        Text(message.content)
            .font(.body)
            .foregroundColor(message.isUser ? .white : .primary)
            .padding(.horizontal, 16)
            .padding(.vertical, 12)
            .background(
                RoundedRectangle(cornerRadius: 18)
                    .fill(message.isUser ? Color.blue : Color(.systemGray5))
            )
            .overlay(
                // Add tail to the bubble
                BubbleTail(isUser: message.isUser)
            )
    }
    
    private var timestampView: some View {
        HStack {
            if message.isUser {
                Spacer()
            }
            
            Text(formatTimestamp(message.timestamp))
                .font(.caption2)
                .foregroundColor(.secondary)
            
            if !message.isUser {
                Spacer()
            }
        }
        .padding(.horizontal, 4)
    }
    
    private func formatTimestamp(_ date: Date) -> String {
        let formatter = DateFormatter()
        let calendar = Calendar.current
        
        if calendar.isToday(date) {
            formatter.timeStyle = .short
            return formatter.string(from: date)
        } else if calendar.isYesterday(date) {
            return "Yesterday"
        } else {
            formatter.dateStyle = .short
            return formatter.string(from: date)
        }
    }
}

struct BubbleTail: View {
    let isUser: Bool
    
    var body: some View {
        VStack {
            if isUser {
                HStack {
                    Spacer()
                    tailShape
                        .fill(Color.blue)
                        .frame(width: 12, height: 12)
                        .offset(x: 6, y: -6)
                }
            } else {
                HStack {
                    tailShape
                        .fill(Color(.systemGray5))
                        .frame(width: 12, height: 12)
                        .offset(x: -6, y: -6)
                        .scaleEffect(x: -1, y: 1)
                    Spacer()
                }
            }
            Spacer()
        }
    }
    
    private var tailShape: some View {
        Path { path in
            path.move(to: CGPoint(x: 0, y: 0))
            path.addCurve(
                to: CGPoint(x: 12, y: 12),
                control1: CGPoint(x: 0, y: 8),
                control2: CGPoint(x: 4, y: 12)
            )
            path.addLine(to: CGPoint(x: 0, y: 12))
            path.closeSubpath()
        }
    }
}

// MARK: - Extended Message View for Rich Content

struct RichMessageBubbleView: View {
    let message: ChatMessage
    @State private var isExpanded = false
    
    var body: some View {
        VStack {
            MessageBubbleView(message: message)
            
            // Add action buttons for Claude messages
            if !message.isUser {
                actionButtons
            }
        }
    }
    
    private var actionButtons: some View {
        HStack(spacing: 12) {
            Button(action: copyMessage) {
                Label("Copy", systemImage: "doc.on.doc")
                    .font(.caption)
                    .foregroundColor(.blue)
            }
            
            Button(action: shareMessage) {
                Label("Share", systemImage: "square.and.arrow.up")
                    .font(.caption)
                    .foregroundColor(.blue)
            }
            
            if message.content.count > 200 {
                Button(action: { isExpanded.toggle() }) {
                    Label(isExpanded ? "Collapse" : "Expand", systemImage: isExpanded ? "chevron.up" : "chevron.down")
                        .font(.caption)
                        .foregroundColor(.blue)
                }
            }
            
            Spacer()
        }
        .padding(.horizontal, 50)
        .padding(.top, 4)
    }
    
    private func copyMessage() {
        UIPasteboard.general.string = message.content
    }
    
    private func shareMessage() {
        let activityViewController = UIActivityViewController(
            activityItems: [message.content],
            applicationActivities: nil
        )
        
        if let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
           let window = windowScene.windows.first {
            window.rootViewController?.present(activityViewController, animated: true)
        }
    }
}

// MARK: - Typing Indicator

struct TypingIndicatorView: View {
    @State private var dotOpacity: [Double] = [0.4, 0.4, 0.4]
    @State private var animationTimer: Timer?
    
    var body: some View {
        HStack {
            messageBubble
            Spacer(minLength: 50)
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 4)
        .onAppear {
            startAnimation()
        }
        .onDisappear {
            stopAnimation()
        }
    }
    
    private var messageBubble: some View {
        HStack {
            Circle()
                .fill(Color.orange)
                .frame(width: 32, height: 32)
                .overlay(
                    Image(systemName: "brain.head.profile")
                        .font(.system(size: 16, weight: .medium))
                        .foregroundColor(.white)
                )
            
            HStack(spacing: 4) {
                ForEach(0..<3, id: \.self) { index in
                    Circle()
                        .fill(Color.gray)
                        .frame(width: 8, height: 8)
                        .opacity(dotOpacity[index])
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 12)
            .background(
                RoundedRectangle(cornerRadius: 18)
                    .fill(Color(.systemGray5))
            )
        }
    }
    
    private func startAnimation() {
        animationTimer = Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { _ in
            withAnimation(.easeInOut(duration: 0.4)) {
                for i in 0..<3 {
                    dotOpacity[i] = dotOpacity[i] == 0.4 ? 1.0 : 0.4
                }
            }
            
            // Stagger the animation
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
                withAnimation(.easeInOut(duration: 0.4)) {
                    dotOpacity[1] = dotOpacity[1] == 0.4 ? 1.0 : 0.4
                }
            }
            
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) {
                withAnimation(.easeInOut(duration: 0.4)) {
                    dotOpacity[2] = dotOpacity[2] == 0.4 ? 1.0 : 0.4
                }
            }
        }
    }
    
    private func stopAnimation() {
        animationTimer?.invalidate()
        animationTimer = nil
    }
}

// MARK: - Message List Container

struct MessageListView: View {
    let messages: [ChatMessage]
    let isLoading: Bool
    
    var body: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 12) {
                    ForEach(messages) { message in
                        RichMessageBubbleView(message: message)
                            .id(message.id)
                    }
                    
                    if isLoading {
                        TypingIndicatorView()
                            .id("typing")
                    }
                }
                .padding()
            }
            .onChange(of: messages.count) { _ in
                scrollToBottom(proxy: proxy)
            }
            .onChange(of: isLoading) { _ in
                if isLoading {
                    scrollToBottom(proxy: proxy)
                }
            }
        }
    }
    
    private func scrollToBottom(proxy: ScrollViewReader) {
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
            withAnimation(.easeOut(duration: 0.3)) {
                if isLoading {
                    proxy.scrollTo("typing", anchor: .bottom)
                } else if let lastMessage = messages.last {
                    proxy.scrollTo(lastMessage.id, anchor: .bottom)
                }
            }
        }
    }
}

#Preview {
    VStack {
        MessageBubbleView(message: ChatMessage(content: "Hello! How can I help you today?", isUser: false))
        MessageBubbleView(message: ChatMessage(content: "I need help with SwiftUI", isUser: true))
        TypingIndicatorView()
    }
    .background(Color(.systemGray6))
}
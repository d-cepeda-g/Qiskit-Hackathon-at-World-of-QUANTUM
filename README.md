# Story Weaver - Multi-Version Storytelling Editor

A powerful, modern web-based storytelling editor that allows you to manage up to **15 different versions** of your story simultaneously. Perfect for writers who want to explore different narrative paths, experiment with alternate storylines, or collaborate on multiple versions of the same story.

## 🌟 Features

### Core Functionality
- **Multi-Version Management**: Create, edit, and manage up to 15 story versions simultaneously
- **Real-time Auto-save**: Your work is automatically saved every 5 seconds
- **Version Comparison**: Side-by-side comparison of different story versions
- **Story Branching**: Create new versions based on existing ones
- **Version Merging**: Combine multiple versions into a single story
- **Import/Export**: Save and load your stories as JSON files

### Editor Features
- **Rich Text Editor**: Clean, distraction-free writing environment
- **Live Statistics**: Real-time word count, character count, and version analytics
- **Undo/Redo**: Full history support with keyboard shortcuts
- **Keyboard Shortcuts**: Efficient writing with common shortcuts
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### User Experience
- **Beautiful UI**: Modern, clean interface with smooth animations
- **Dark Theme Ready**: Professional gradient background with glass morphism
- **Intuitive Navigation**: Easy version switching and management
- **Visual Feedback**: Toast notifications and status indicators
- **Local Storage**: Your stories persist between browser sessions

## 🚀 Getting Started

### Quick Start
1. Clone or download this repository
2. Open `index.html` in your web browser
3. Start writing your story!

### No Dependencies Required
This is a pure HTML/CSS/JavaScript application with no build process or external dependencies (except for Font Awesome icons and Google Fonts, which are loaded from CDN).

## 📖 How to Use

### Creating Your First Story
1. **Start Writing**: Click in the main editor area and begin typing your story
2. **Add Versions**: Click the "+" button next to "Story Versions" to create new versions
3. **Switch Versions**: Click on any version in the sidebar to switch to it
4. **Edit Titles**: Click the edit icon next to the version title to rename it

### Managing Versions
- **Create New Version**: Use the "+" button or Ctrl+N
- **Create Branch**: Use "Create Branch" button to copy current version
- **Duplicate Version**: Click the copy icon on any version
- **Delete Version**: Click the trash icon on any version (requires confirmation)

### Version Tools
- **Compare Versions**: Select two versions to see them side-by-side
- **Merge Versions**: Combine multiple versions into one
- **Export All**: Download all versions as a JSON file
- **Import Stories**: Load previously exported stories

### Keyboard Shortcuts
- `Ctrl+S` (or `Cmd+S`): Save story
- `Ctrl+Z` (or `Cmd+Z`): Undo
- `Ctrl+Shift+Z` (or `Cmd+Shift+Z`): Redo
- `Ctrl+N` (or `Cmd+N`): Create new version

## 🔧 Technical Details

### Browser Support
- Chrome/Chromium 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### Storage
- Uses browser's `localStorage` for persistence
- No server required - everything runs locally
- Stories are automatically saved every 5 seconds
- Manual save available with Ctrl+S

### File Format
Exported stories use JSON format with this structure:
```json
{
  "currentVersionId": 1,
  "versions": [
    {
      "id": 1,
      "title": "Main Story",
      "content": "Your story content...",
      "wordCount": 150,
      "charCount": 890,
      "created": "2024-01-15T10:30:00.000Z",
      "modified": "2024-01-15T11:45:00.000Z",
      "parentId": null
    }
  ],
  "exportDate": "2024-01-15T11:45:00.000Z",
  "appVersion": "1.0.0"
}
```

## 🎨 Customization

### Styling
The application uses CSS custom properties and can be easily customized by modifying `styles.css`. Key areas for customization:

- **Colors**: Update the gradient backgrounds and accent colors
- **Typography**: Change fonts (currently using Inter for UI and Georgia for editor)
- **Layout**: Adjust sidebar width, editor padding, etc.
- **Animations**: Modify transition durations and effects

### Functionality
The JavaScript is organized in a single class (`StoryWeaver`) making it easy to extend:

- **Add new version operations**: Extend the version management methods
- **Custom export formats**: Modify the export functionality
- **Enhanced comparison**: Improve the version comparison algorithm
- **Collaboration features**: Add real-time collaboration (would require a backend)

## 📊 Analytics & Statistics

The application provides comprehensive analytics:

### Per Version
- Word count
- Character count
- Creation date
- Last modified date
- Parent version (for branches)

### Overall
- Total words across all versions
- Total characters across all versions
- Number of active versions
- Version hierarchy visualization

## 💡 Use Cases

### Creative Writing
- **Alternate Endings**: Write multiple endings for your story
- **Character Development**: Explore different character arcs
- **Plot Variations**: Try different plot directions
- **Genre Experiments**: Adapt the same story for different genres

### Professional Writing
- **Client Revisions**: Maintain different versions for client feedback
- **A/B Testing**: Test different approaches with readers
- **Collaboration**: Work with editors while preserving original versions
- **Version Control**: Track changes and maintain edit history

### Educational
- **Creative Writing Classes**: Students can explore different narrative approaches
- **Peer Review**: Share different versions for feedback
- **Writing Exercises**: Practice different writing styles on the same story
- **Portfolio Development**: Maintain multiple drafts and versions

## 🚀 Future Enhancements

Potential features for future versions:
- **Collaborative Editing**: Real-time collaboration with other writers
- **Cloud Sync**: Sync stories across devices
- **Advanced Diff**: More sophisticated version comparison with change highlighting
- **Writing Goals**: Set and track daily/weekly writing targets
- **Export Formats**: PDF, EPUB, Word document export
- **Themes**: Multiple UI themes and editor color schemes
- **Plugins**: Extensible architecture for custom features

## 🐛 Troubleshooting

### Common Issues

**Stories not saving**
- Ensure your browser supports localStorage
- Check if you have sufficient storage space
- Try refreshing the page

**Performance issues with many versions**
- The app is optimized for up to 15 versions
- Consider exporting and starting fresh if experiencing slowdowns
- Close unnecessary browser tabs to free up memory

**Import/Export problems**
- Ensure JSON files are valid and not corrupted
- Check file size limits (most browsers handle files up to several MB)
- Try exporting without metadata if files are too large

## 📄 License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute as needed.

## 🤝 Contributing

Contributions are welcome! Whether it's bug fixes, feature improvements, or documentation updates, feel free to submit pull requests or open issues.

---

**Happy Writing!** 📝✨

Create amazing stories with multiple versions and explore the endless possibilities of narrative creativity.





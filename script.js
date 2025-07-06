// Story Weaver - Multi-Version Storytelling Editor
class StoryWeaver {
    constructor() {
        this.maxVersions = 15;
        this.currentVersionId = 1;
        this.versions = new Map();
        this.history = [];
        this.historyIndex = -1;
        this.autoSaveInterval = null;
        this.isEditing = false;

        // Initialize with first version
        this.createVersion('Main Story', true);
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadFromStorage();
        this.renderVersionList();
        this.startAutoSave();
        this.updateUI();
    }

    bindEvents() {
        // Header controls
        document.getElementById('newStoryBtn').addEventListener('click', () => this.newStory());
        document.getElementById('exportBtn').addEventListener('click', () => this.showExportModal());
        document.getElementById('importBtn').addEventListener('click', () => this.showImportModal());

        // Version management
        document.getElementById('addVersionBtn').addEventListener('click', () => this.addVersion());
        document.getElementById('compareBtn').addEventListener('click', () => this.showCompareModal());
        document.getElementById('mergeBtn').addEventListener('click', () => this.mergeVersions());
        document.getElementById('branchBtn').addEventListener('click', () => this.createBranch());

        // Editor controls
        document.getElementById('editTitleBtn').addEventListener('click', () => this.editVersionTitle());
        document.getElementById('undoBtn').addEventListener('click', () => this.undo());
        document.getElementById('redoBtn').addEventListener('click', () => this.redo());
        document.getElementById('saveBtn').addEventListener('click', () => this.saveToStorage());

        // Editor content
        const editor = document.getElementById('storyEditor');
        editor.addEventListener('input', () => this.onEditorChange());
        editor.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));

        // Version title editing
        const titleInput = document.getElementById('versionTitleInput');
        titleInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.saveVersionTitle();
            } else if (e.key === 'Escape') {
                this.cancelEditTitle();
            }
        });
        titleInput.addEventListener('blur', () => this.saveVersionTitle());

        // Modal events
        this.bindModalEvents();
    }

    bindModalEvents() {
        // Compare modal
        document.getElementById('closeCompareModal').addEventListener('click', () => this.hideModal('compareModal'));
        document.getElementById('runCompareBtn').addEventListener('click', () => this.runComparison());

        // Import/Export modal
        document.getElementById('closeImportExportModal').addEventListener('click', () => this.hideModal('importExportModal'));
        document.getElementById('processImportBtn').addEventListener('click', () => this.processImport());
        document.getElementById('downloadExportBtn').addEventListener('click', () => this.downloadExport());

        // File input
        document.getElementById('fileInput').addEventListener('change', (e) => this.handleFileSelect(e));

        // Modal backdrop clicks
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.hideModal(modal.id);
                }
            });
        });
    }

    createVersion(title = `Version ${this.versions.size + 1}`, isDefault = false) {
        if (this.versions.size >= this.maxVersions) {
            this.showNotification('Maximum number of versions reached (15)', 'warning');
            return null;
        }

        const versionId = isDefault ? 1 : Date.now();
        const version = {
            id: versionId,
            title: title,
            content: '',
            wordCount: 0,
            charCount: 0,
            created: new Date().toISOString(),
            modified: new Date().toISOString(),
            parentId: isDefault ? null : this.currentVersionId
        };

        this.versions.set(versionId, version);
        
        if (!isDefault) {
            this.currentVersionId = versionId;
        }

        return versionId;
    }

    addVersion() {
        const versionId = this.createVersion();
        if (versionId) {
            this.renderVersionList();
            this.switchToVersion(versionId);
            this.saveToStorage();
        }
    }

    createBranch() {
        const currentVersion = this.versions.get(this.currentVersionId);
        const versionId = this.createVersion(`Branch from ${currentVersion.title}`);
        
        if (versionId) {
            const newVersion = this.versions.get(versionId);
            newVersion.content = currentVersion.content;
            newVersion.wordCount = currentVersion.wordCount;
            newVersion.charCount = currentVersion.charCount;
            
            this.renderVersionList();
            this.switchToVersion(versionId);
            this.saveToStorage();
            this.showNotification('Branch created successfully', 'success');
        }
    }

    switchToVersion(versionId) {
        // Save current version content before switching
        this.saveCurrentVersion();
        
        this.currentVersionId = versionId;
        const version = this.versions.get(versionId);
        
        // Update editor content
        document.getElementById('storyEditor').value = version.content;
        
        // Update UI
        this.updateVersionTitle();
        this.updateVersionList();
        this.updateWordCount();
        this.updateUI();
    }

    deleteVersion(versionId) {
        if (this.versions.size <= 1) {
            this.showNotification('Cannot delete the last version', 'warning');
            return;
        }

        if (confirm('Are you sure you want to delete this version?')) {
            this.versions.delete(versionId);
            
            // Switch to first available version if current was deleted
            if (this.currentVersionId === versionId) {
                this.currentVersionId = this.versions.keys().next().value;
                this.switchToVersion(this.currentVersionId);
            }
            
            this.renderVersionList();
            this.saveToStorage();
            this.showNotification('Version deleted', 'success');
        }
    }

    duplicateVersion(versionId) {
        const originalVersion = this.versions.get(versionId);
        const newVersionId = this.createVersion(`Copy of ${originalVersion.title}`);
        
        if (newVersionId) {
            const newVersion = this.versions.get(newVersionId);
            newVersion.content = originalVersion.content;
            newVersion.wordCount = originalVersion.wordCount;
            newVersion.charCount = originalVersion.charCount;
            
            this.renderVersionList();
            this.switchToVersion(newVersionId);
            this.saveToStorage();
            this.showNotification('Version duplicated', 'success');
        }
    }

    saveCurrentVersion() {
        if (this.currentVersionId) {
            const version = this.versions.get(this.currentVersionId);
            const editor = document.getElementById('storyEditor');
            
            version.content = editor.value;
            version.modified = new Date().toISOString();
            this.updateWordCount();
        }
    }

    onEditorChange() {
        this.isEditing = true;
        this.updateWordCount();
        this.updateAutoSaveStatus('editing');
        
        // Add to history for undo/redo
        this.addToHistory();
    }

    updateWordCount() {
        const editor = document.getElementById('storyEditor');
        const content = editor.value;
        const words = content.trim() === '' ? 0 : content.trim().split(/\s+/).length;
        const chars = content.length;

        // Update current version
        if (this.currentVersionId) {
            const version = this.versions.get(this.currentVersionId);
            version.wordCount = words;
            version.charCount = chars;
        }

        // Update UI
        document.getElementById('currentWords').textContent = words.toLocaleString();
        document.getElementById('currentChars').textContent = chars.toLocaleString();
        
        // Update total stats
        this.updateTotalStats();
    }

    updateTotalStats() {
        let totalWords = 0;
        let totalChars = 0;

        this.versions.forEach(version => {
            totalWords += version.wordCount;
            totalChars += version.charCount;
        });

        document.getElementById('totalWords').textContent = totalWords.toLocaleString();
        document.getElementById('totalChars').textContent = totalChars.toLocaleString();
        document.getElementById('versionCount').textContent = this.versions.size;
    }

    renderVersionList() {
        const versionList = document.getElementById('versionList');
        versionList.innerHTML = '';

        Array.from(this.versions.values())
            .sort((a, b) => new Date(a.created) - new Date(b.created))
            .forEach(version => {
                const versionElement = this.createVersionElement(version);
                versionList.appendChild(versionElement);
            });

        this.updateVersionList();
    }

    createVersionElement(version) {
        const div = document.createElement('div');
        div.className = 'version-item';
        div.dataset.versionId = version.id;

        const modified = new Date(version.modified).toLocaleDateString();
        
        div.innerHTML = `
            <div class="version-info">
                <div class="version-title">${this.escapeHtml(version.title)}</div>
                <div class="version-meta">
                    ${version.wordCount.toLocaleString()} words • Modified ${modified}
                </div>
            </div>
            <div class="version-actions">
                <button class="btn btn-ghost btn-small" onclick="storyWeaver.duplicateVersion(${version.id})" title="Duplicate">
                    <i class="fas fa-copy"></i>
                </button>
                <button class="btn btn-ghost btn-small" onclick="storyWeaver.deleteVersion(${version.id})" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;

        div.addEventListener('click', (e) => {
            if (!e.target.closest('.version-actions')) {
                this.switchToVersion(version.id);
            }
        });

        return div;
    }

    updateVersionList() {
        document.querySelectorAll('.version-item').forEach(item => {
            const versionId = parseInt(item.dataset.versionId);
            item.classList.toggle('active', versionId === this.currentVersionId);
        });
    }

    updateVersionTitle() {
        const version = this.versions.get(this.currentVersionId);
        document.getElementById('currentVersionTitle').textContent = `Version ${Array.from(this.versions.keys()).indexOf(this.currentVersionId) + 1}: ${version.title}`;
    }

    editVersionTitle() {
        const titleElement = document.getElementById('currentVersionTitle');
        const inputElement = document.getElementById('versionTitleInput');
        const version = this.versions.get(this.currentVersionId);

        titleElement.classList.add('hidden');
        inputElement.classList.remove('hidden');
        inputElement.value = version.title;
        inputElement.focus();
        inputElement.select();
    }

    saveVersionTitle() {
        const titleElement = document.getElementById('currentVersionTitle');
        const inputElement = document.getElementById('versionTitleInput');
        const version = this.versions.get(this.currentVersionId);

        const newTitle = inputElement.value.trim();
        if (newTitle) {
            version.title = newTitle;
            version.modified = new Date().toISOString();
            this.updateVersionTitle();
            this.renderVersionList();
            this.saveToStorage();
        }

        this.cancelEditTitle();
    }

    cancelEditTitle() {
        document.getElementById('currentVersionTitle').classList.remove('hidden');
        document.getElementById('versionTitleInput').classList.add('hidden');
    }

    // Auto-save functionality
    startAutoSave() {
        this.autoSaveInterval = setInterval(() => {
            if (this.isEditing) {
                this.saveCurrentVersion();
                this.saveToStorage();
                this.updateAutoSaveStatus('saved');
                this.isEditing = false;
            }
        }, 5000); // Auto-save every 5 seconds
    }

    updateAutoSaveStatus(status) {
        const statusElement = document.getElementById('autoSaveStatus');
        const now = new Date().toLocaleTimeString();

        switch (status) {
            case 'editing':
                statusElement.innerHTML = '<i class="fas fa-circle text-warning"></i> Editing...';
                break;
            case 'saved':
                statusElement.innerHTML = '<i class="fas fa-circle text-success"></i> Auto-saved';
                document.getElementById('lastSaved').textContent = now;
                break;
            default:
                statusElement.innerHTML = '<i class="fas fa-circle text-success"></i> Auto-save enabled';
        }
    }

    // History and Undo/Redo
    addToHistory() {
        const editor = document.getElementById('storyEditor');
        const state = {
            versionId: this.currentVersionId,
            content: editor.value,
            cursorPosition: editor.selectionStart
        };

        // Remove any history after current index
        this.history = this.history.slice(0, this.historyIndex + 1);
        this.history.push(state);
        
        // Limit history size
        if (this.history.length > 50) {
            this.history.shift();
        } else {
            this.historyIndex++;
        }

        this.updateUndoRedoButtons();
    }

    undo() {
        if (this.historyIndex > 0) {
            this.historyIndex--;
            this.restoreFromHistory();
        }
    }

    redo() {
        if (this.historyIndex < this.history.length - 1) {
            this.historyIndex++;
            this.restoreFromHistory();
        }
    }

    restoreFromHistory() {
        const state = this.history[this.historyIndex];
        const editor = document.getElementById('storyEditor');
        
        editor.value = state.content;
        editor.setSelectionRange(state.cursorPosition, state.cursorPosition);
        
        this.updateWordCount();
        this.updateUndoRedoButtons();
    }

    updateUndoRedoButtons() {
        document.getElementById('undoBtn').disabled = this.historyIndex <= 0;
        document.getElementById('redoBtn').disabled = this.historyIndex >= this.history.length - 1;
    }

    // Version Comparison
    showCompareModal() {
        const modal = document.getElementById('compareModal');
        const select1 = document.getElementById('compareVersion1');
        const select2 = document.getElementById('compareVersion2');

        // Populate version selects
        this.populateVersionSelects([select1, select2]);
        
        modal.classList.add('active');
    }

    populateVersionSelects(selects) {
        selects.forEach(select => {
            select.innerHTML = '<option value="">Select version...</option>';
            this.versions.forEach(version => {
                const option = document.createElement('option');
                option.value = version.id;
                option.textContent = `${version.title} (${version.wordCount} words)`;
                select.appendChild(option);
            });
        });
    }

    runComparison() {
        const version1Id = parseInt(document.getElementById('compareVersion1').value);
        const version2Id = parseInt(document.getElementById('compareVersion2').value);

        if (!version1Id || !version2Id) {
            this.showNotification('Please select two versions to compare', 'warning');
            return;
        }

        const version1 = this.versions.get(version1Id);
        const version2 = this.versions.get(version2Id);

        const resultDiv = document.getElementById('comparisonResult');
        resultDiv.innerHTML = `
            <div class="comparison-section">
                <div class="comparison-version">
                    <div class="comparison-header">${this.escapeHtml(version1.title)}</div>
                    <div>${this.escapeHtml(version1.content)}</div>
                </div>
                <div class="comparison-version">
                    <div class="comparison-header">${this.escapeHtml(version2.title)}</div>
                    <div>${this.escapeHtml(version2.content)}</div>
                </div>
            </div>
        `;
    }

    // Merge Versions
    mergeVersions() {
        // Simple merge - this could be expanded with more sophisticated merging
        const selectedVersions = Array.from(document.querySelectorAll('.version-item.active'));
        
        if (selectedVersions.length < 2) {
            this.showNotification('Please select multiple versions to merge', 'warning');
            return;
        }

        const mergeId = this.createVersion('Merged Version');
        if (mergeId) {
            const mergedVersion = this.versions.get(mergeId);
            let mergedContent = '';

            selectedVersions.forEach((item, index) => {
                const versionId = parseInt(item.dataset.versionId);
                const version = this.versions.get(versionId);
                mergedContent += `\n\n=== ${version.title} ===\n\n${version.content}`;
            });

            mergedVersion.content = mergedContent.trim();
            this.switchToVersion(mergeId);
            this.showNotification('Versions merged successfully', 'success');
        }
    }

    // Import/Export
    showImportModal() {
        const modal = document.getElementById('importExportModal');
        document.getElementById('importExportTitle').textContent = 'Import Stories';
        document.getElementById('importSection').classList.remove('hidden');
        document.getElementById('exportSection').classList.add('hidden');
        modal.classList.add('active');
    }

    showExportModal() {
        const modal = document.getElementById('importExportModal');
        document.getElementById('importExportTitle').textContent = 'Export Stories';
        document.getElementById('importSection').classList.add('hidden');
        document.getElementById('exportSection').classList.remove('hidden');
        modal.classList.add('active');
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file && file.type === 'application/json') {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const data = JSON.parse(e.target.result);
                    this.importData = data;
                    this.showNotification('File loaded successfully. Click "Import Stories" to proceed.', 'success');
                } catch (error) {
                    this.showNotification('Invalid JSON file', 'error');
                }
            };
            reader.readAsText(file);
        }
    }

    processImport() {
        if (!this.importData) {
            this.showNotification('Please select a file first', 'warning');
            return;
        }

        try {
            // Clear current versions
            this.versions.clear();
            
            // Import versions
            if (this.importData.versions) {
                this.importData.versions.forEach(versionData => {
                    this.versions.set(versionData.id, versionData);
                });
            }

            // Set current version
            this.currentVersionId = this.importData.currentVersionId || this.versions.keys().next().value;
            
            // Update UI
            this.renderVersionList();
            this.switchToVersion(this.currentVersionId);
            this.saveToStorage();
            
            this.hideModal('importExportModal');
            this.showNotification('Stories imported successfully', 'success');
        } catch (error) {
            this.showNotification('Error importing stories', 'error');
        }
    }

    downloadExport() {
        const exportAllVersions = document.getElementById('exportAllVersions').checked;
        const includeMetadata = document.getElementById('includeMetadata').checked;

        const exportData = {
            currentVersionId: this.currentVersionId,
            versions: [],
            exportDate: new Date().toISOString(),
            appVersion: '1.0.0'
        };

        this.versions.forEach(version => {
            const versionData = {
                id: version.id,
                title: version.title,
                content: version.content
            };

            if (includeMetadata) {
                versionData.wordCount = version.wordCount;
                versionData.charCount = version.charCount;
                versionData.created = version.created;
                versionData.modified = version.modified;
                versionData.parentId = version.parentId;
            }

            exportData.versions.push(versionData);
        });

        const dataStr = JSON.stringify(exportData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `story-weaver-export-${new Date().toISOString().split('T')[0]}.json`;
        link.click();

        this.hideModal('importExportModal');
        this.showNotification('Stories exported successfully', 'success');
    }

    // Storage
    saveToStorage() {
        const data = {
            versions: Array.from(this.versions.entries()),
            currentVersionId: this.currentVersionId,
            lastSaved: new Date().toISOString()
        };

        localStorage.setItem('storyWeaver', JSON.stringify(data));
    }

    loadFromStorage() {
        const saved = localStorage.getItem('storyWeaver');
        if (saved) {
            try {
                const data = JSON.parse(saved);
                this.versions = new Map(data.versions);
                this.currentVersionId = data.currentVersionId;
                
                // Ensure we have at least one version
                if (this.versions.size === 0) {
                    this.createVersion('Main Story', true);
                }

                this.switchToVersion(this.currentVersionId);
            } catch (error) {
                console.error('Error loading from storage:', error);
            }
        }
    }

    // Utility functions
    newStory() {
        if (confirm('Are you sure you want to start a new story? This will clear all current versions.')) {
            this.versions.clear();
            this.createVersion('Main Story', true);
            this.currentVersionId = 1;
            this.history = [];
            this.historyIndex = -1;
            
            document.getElementById('storyEditor').value = '';
            this.renderVersionList();
            this.updateUI();
            this.saveToStorage();
            
            this.showNotification('New story started', 'success');
        }
    }

    updateUI() {
        this.updateVersionTitle();
        this.updateWordCount();
        this.updateTotalStats();
        this.updateUndoRedoButtons();
    }

    hideModal(modalId) {
        document.getElementById(modalId).classList.remove('active');
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#48bb78' : type === 'warning' ? '#ed8936' : type === 'error' ? '#e53e3e' : '#667eea'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 10);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    handleKeyboardShortcuts(event) {
        if (event.ctrlKey || event.metaKey) {
            switch (event.key) {
                case 's':
                    event.preventDefault();
                    this.saveToStorage();
                    this.showNotification('Story saved', 'success');
                    break;
                case 'z':
                    if (event.shiftKey) {
                        event.preventDefault();
                        this.redo();
                    } else {
                        event.preventDefault();
                        this.undo();
                    }
                    break;
                case 'n':
                    event.preventDefault();
                    this.addVersion();
                    break;
            }
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application
let storyWeaver;

document.addEventListener('DOMContentLoaded', () => {
    storyWeaver = new StoryWeaver();
});

// Export for global access
window.storyWeaver = storyWeaver;
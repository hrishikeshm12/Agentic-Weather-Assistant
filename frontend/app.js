/**
 * Weather Agent Frontend
 * Handles user interaction and communication with the backend agent
 */

const API_URL = 'http://localhost:8000';

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const queryForm = document.getElementById('queryForm');
const queryInput = document.getElementById('queryInput');
const sendButton = document.getElementById('sendButton');
const loadingIndicator = document.getElementById('loadingIndicator');
const examplesList = document.getElementById('examplesList');

// State
let isLoading = false;

/**
 * Initialize the application
 */
async function init() {
    // Load example queries
    await loadExamples();

    // Add event listeners
    queryForm.addEventListener('submit', handleQuerySubmit);
    queryInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
            queryForm.dispatchEvent(new Event('submit'));
        }
    });

    // Check backend health
    checkBackendHealth();
}

/**
 * Load example queries from backend
 */
async function loadExamples() {
    try {
        const response = await fetch(`${API_URL}/examples`);
        if (!response.ok) throw new Error('Failed to load examples');

        const data = await response.json();
        const examples = data.examples || [];

        examplesList.innerHTML = examples
            .map(
                (example) =>
                    `<button type="button" class="example-button" onclick="setQuery('${example.replace(/'/g, "\\'")}')">
                        ${escapeHtml(example)}
                    </button>`
            )
            .join('');
    } catch (error) {
        console.error('Error loading examples:', error);
    }
}

/**
 * Set query input and focus
 */
function setQuery(query) {
    queryInput.value = query;
    queryInput.focus();
}

/**
 * Handle form submission
 */
async function handleQuerySubmit(e) {
    e.preventDefault();

    const query = queryInput.value.trim();
    if (!query || isLoading) return;

    // Clear input
    queryInput.value = '';

    // Add user message to chat
    addMessage(query, 'user');

    // Send query to agent
    await sendQuery(query);
}

/**
 * Send query to backend agent
 */
async function sendQuery(query) {
    isLoading = true;
    setUILoading(true);

    try {
        const response = await fetch(`${API_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Query failed');
        }

        const data = await response.json();

        if (data.success) {
            addMessage(data.response, 'agent');
        } else {
            addMessage(`Error: ${data.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Error sending query:', error);
        addMessage(
            `I encountered an error: ${error.message}. Please try again.`,
            'error'
        );
    } finally {
        isLoading = false;
        setUILoading(false);
        queryInput.focus();
    }
}

/**
 * Add message to chat
 */
function addMessage(content, role = 'user') {
    // Remove welcome message if this is the first user message
    const welcomeMessage = chatMessages.querySelector('.welcome-message');
    if (welcomeMessage && role === 'user') {
        welcomeMessage.remove();
    }

    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    // Parse markdown and format content
    const formattedContent = parseMarkdown(content);
    messageContent.innerHTML = formattedContent;

    messageDiv.appendChild(messageContent);

    // Add timestamp
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
    });
    messageDiv.appendChild(timestamp);

    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Set UI loading state
 */
function setUILoading(loading) {
    if (loading) {
        loadingIndicator.classList.remove('hidden');
        sendButton.disabled = true;
    } else {
        loadingIndicator.classList.add('hidden');
        sendButton.disabled = false;
    }
}

/**
 * Check backend health
 */
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (!response.ok) {
            console.warn('Backend health check failed');
            addMessage(
                'ℹ️ Backend is initializing. Please wait a moment...',
                'system'
            );
        }
    } catch (error) {
        console.error('Backend not reachable:', error);
        addMessage(
            '⚠️ Cannot reach the backend server. Make sure it is running on ' +
                API_URL,
            'error'
        );
    }
}

/**
 * Parse markdown and convert to safe HTML
 */
function parseMarkdown(text) {
    // Escape HTML first
    const div = document.createElement('div');
    div.textContent = text;
    let html = div.innerHTML;

    // Now convert markdown (on already-escaped HTML)
    // This prevents XSS while allowing markdown rendering

    // Bold: **text** -> <strong>text</strong>
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic: *text* -> <em>text</em> (but not in bold)
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Code: `code` -> <code>code</code>
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Handle paragraphs: split by double newlines, keep single newlines within paragraphs
    let paragraphs = html.split(/\n\n+/);
    paragraphs = paragraphs.map(para => {
        // Convert bullet points: - item -> • item (with proper spacing)
        para = para.replace(/^\s*-\s+/gm, '• ');
        // Convert single newlines to <br>
        para = para.replace(/\n/g, '<br>');
        return `<div style="margin-bottom: 10px; line-height: 1.6;">${para}</div>`;
    });

    return paragraphs.join('');
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Initialize app when DOM is ready
 */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

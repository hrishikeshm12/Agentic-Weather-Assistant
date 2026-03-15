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

// Example queries (matching backend/prompts.py)
const EXAMPLE_QUERIES = [
    "What's the weather like in New York?",
    "Will it rain in London tomorrow?",
    "Compare the weather in Tokyo and Sydney",
    "Is it a good day for outdoor activities in San Francisco?",
    "What's the forecast for Paris next week?"
];

/**
 * Initialize the application
 */
async function init() {
    // Render example queries
    renderExamples();

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
 * Render example query buttons into the DOM
 */
function renderExamples() {
    const target = document.getElementById('examplesList');
    if (!target) {
        console.error('examplesList element not found');
        return;
    }

    let html = '';
    for (let i = 0; i < EXAMPLE_QUERIES.length; i++) {
        const example = EXAMPLE_QUERIES[i];
        const safeExample = example.replace(/'/g, "\\'").replace(/"/g, '&quot;');
        html += '<button type="button" class="example-button" onclick="setQuery(\'' + safeExample + '\')">' + example + '</button>';
    }
    target.innerHTML = html;
    console.log('Rendered', EXAMPLE_QUERIES.length, 'examples into', target);
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
            // Show tool calls if any (agent transparency)
            if (data.tool_calls && data.tool_calls.length > 0) {
                addToolCallsMessage(data.tool_calls);
            }
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
 * Show tool calls the agent made (agent transparency)
 */
function addToolCallsMessage(toolCalls) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message tool-calls';

    const content = document.createElement('div');
    content.className = 'tool-calls-content';

    const header = document.createElement('div');
    header.className = 'tool-calls-header';
    header.innerHTML = '<span class="tool-icon">&#9881;</span> Agent Actions';
    content.appendChild(header);

    toolCalls.forEach((tc) => {
        const item = document.createElement('div');
        item.className = `tool-call-item ${tc.status}`;

        const toolName = tc.tool.replace(/_/g, ' ');
        const inputStr = Object.entries(tc.input || {})
            .map(([k, v]) => `${k}: ${v}`)
            .join(', ');

        item.innerHTML = `
            <span class="tool-status-icon">${tc.status === 'success' ? '&#10003;' : '&#10007;'}</span>
            <span class="tool-name">${escapeHtml(toolName)}</span>
            <span class="tool-input">(${escapeHtml(inputStr)})</span>
            ${tc.result_preview ? `<span class="tool-preview">&rarr; ${escapeHtml(tc.result_preview)}</span>` : ''}
        `;
        content.appendChild(item);
    });

    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
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
 * Reset conversation
 */
async function resetConversation() {
    try {
        await fetch(`${API_URL}/reset`, { method: 'POST' });
    } catch (error) {
        console.error('Error resetting conversation:', error);
    }

    // Clear chat UI and rebuild welcome message
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <h2>Welcome to Weather Agent</h2>
            <p>Ask me about weather in any city. I'll provide current conditions, forecasts, and helpful insights.</p>
            <p class="feature-note">Multi-turn conversations supported - ask follow-up questions!</p>
            <div class="example-queries">
                <p>Try asking:</p>
                <div id="examplesList"></div>
            </div>
        </div>
    `;

    // Re-render example buttons into the new DOM element
    renderExamples();
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
                'Backend is initializing. Please wait a moment...',
                'system'
            );
        }
    } catch (error) {
        console.error('Backend not reachable:', error);
        addMessage(
            'Cannot reach the backend server. Make sure it is running on ' +
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

    // Bold: **text** -> <strong>text</strong>
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic: *text* -> <em>text</em> (but not in bold)
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Code: `code` -> <code>code</code>
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Handle paragraphs: split by double newlines
    let paragraphs = html.split(/\n\n+/);
    paragraphs = paragraphs.map(para => {
        // Convert bullet points: - item -> bullet item
        para = para.replace(/^\s*-\s+/gm, '&bull; ');
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

/**
 * Mayank Classes - AI Academic Counselor Chatbot
 * Powered by Gemini API & Django Backend
 */

(function () {
  'use strict';

  let chatHistory = [];
  let isAwaitingResponse = false;

  const preTemplates = [
    { label: '💰 Fee Structure', query: 'What is the fee structure for NEET, JEE and Foundation courses?' },
    { label: '🩺 NEET Medical', query: 'Tell me about the NEET 2-Year Comprehensive program details and discounted fees' },
    { label: '⚛️ IIT-JEE Prep', query: 'What are the features and fees for IIT-JEE Main & Advanced courses?' },
    { label: '🎓 Foundation 6-10', query: 'What courses do you have for Class 6 to 10 Foundation and Olympiads?' },
    { label: '📝 Free Demo Class', query: 'How can I book a free demo class and scholarship test?' },
    { label: '👨‍🏫 Faculty Mentors', query: 'Who are the senior faculty mentors and what are their qualifications?' },
    { label: '🏆 CUET & NDA', query: 'Do you offer coaching for CUET (UG) and UPSC NDA entrance exams?' },
    { label: '📞 Contact Helpline', query: 'What is your admissions helpline and center contact info?' }
  ];

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function initChatbot() {
    const launcher = document.getElementById('ai-chat-launcher');
    const windowEl = document.getElementById('ai-chat-window');
    const closeBtn = document.getElementById('ai-chat-close-btn');
    const clearBtn = document.getElementById('ai-chat-clear-btn');
    const form = document.getElementById('ai-chat-form');
    const input = document.getElementById('ai-chat-input');
    const chipsContainer = document.getElementById('ai-chat-chips');

    if (!launcher || !windowEl) return;

    // Render pre-template chips
    if (chipsContainer) {
      chipsContainer.innerHTML = '';
      preTemplates.forEach(t => {
        const chip = document.createElement('button');
        chip.type = 'button';
        chip.className = 'ai-chat-chip';
        chip.textContent = t.label;
        chip.setAttribute('data-query', t.query);
        chip.addEventListener('click', () => {
          sendUserMessage(t.query);
        });
        chipsContainer.appendChild(chip);
      });
    }

    // Toggle Chat Window
    launcher.addEventListener('click', () => {
      const isOpen = windowEl.classList.contains('active');
      if (isOpen) {
        closeChat();
      } else {
        openChat();
      }
    });

    if (closeBtn) closeBtn.addEventListener('click', closeChat);
    if (clearBtn) clearBtn.addEventListener('click', clearChat);

    // Form submit
    if (form && input) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = input.value.trim();
        if (text && !isAwaitingResponse) {
          sendUserMessage(text);
          input.value = '';
        }
      });

      // Enter key
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          form.dispatchEvent(new Event('submit'));
        }
      });
    }

    // Auto show hint pill for 6 seconds then hide
    const hintPill = document.getElementById('ai-chat-launcher-hint');
    if (hintPill) {
      setTimeout(() => {
        hintPill.classList.add('fade-out');
      }, 6000);
    }
  }

  function openChat() {
    const windowEl = document.getElementById('ai-chat-window');
    const launcher = document.getElementById('ai-chat-launcher');
    const input = document.getElementById('ai-chat-input');
    if (!windowEl) return;

    windowEl.classList.add('active');
    if (launcher) launcher.classList.add('chat-open');
    if (input) setTimeout(() => input.focus(), 250);

    scrollToBottom();
  }

  function closeChat() {
    const windowEl = document.getElementById('ai-chat-window');
    const launcher = document.getElementById('ai-chat-launcher');
    if (!windowEl) return;

    windowEl.classList.remove('active');
    if (launcher) launcher.classList.remove('chat-open');
  }

  function clearChat() {
    const messagesEl = document.getElementById('ai-chat-messages');
    if (!messagesEl) return;
    chatHistory = [];

    messagesEl.innerHTML = `
      <div class="ai-msg-bubble ai-msg-bot">
        <div class="ai-msg-avatar">🤖</div>
        <div class="ai-msg-content">
          <p>👋 Hello! I am your <strong>Mayank Classes AI Academic Counselor</strong>.</p>
          <p>Ask me about our courses (NEET, JEE, Foundation 6–10, CUET, NDA), fee structures, faculty mentors, batch timings, or how to book a <strong>Free Demo Class</strong>!</p>
          <div class="ai-msg-prompt-hint">💡 Tap any quick topic above or type your question:</div>
        </div>
      </div>
    `;
    scrollToBottom();
  }

  function parseMarkdownTables(text) {
    if (!text) return '';
    const lines = text.split('\n');
    let inTable = false;
    let tableRows = [];
    let output = [];

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (line.startsWith('|') && line.endsWith('|')) {
        // Skip markdown separator row like | :--- | :--- |
        if (/^\|[\s\-:]+(\|[\s\-:]+)+\|$/.test(line)) {
          continue;
        }
        const cells = line.split('|').slice(1, -1).map(c => c.trim());
        if (!inTable) {
          inTable = true;
          tableRows = [{ type: 'header', cells }];
        } else {
          tableRows.push({ type: 'row', cells });
        }
      } else {
        if (inTable) {
          output.push(renderTableHtml(tableRows));
          inTable = false;
          tableRows = [];
        }
        output.push(lines[i]);
      }
    }

    if (inTable) {
      output.push(renderTableHtml(tableRows));
    }

    return output.join('\n');
  }

  function renderTableHtml(rows) {
    if (!rows || rows.length === 0) return '';
    let html = '<div class="ai-table-wrap"><table class="ai-chat-table">';
    rows.forEach((r, idx) => {
      if (r.type === 'header' || idx === 0) {
        html += '<thead><tr>';
        r.cells.forEach(c => { 
          const formatted = c.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
          html += `<th>${formatted}</th>`; 
        });
        html += '</tr></thead><tbody>';
      } else {
        html += '<tr>';
        r.cells.forEach(c => { 
          const formatted = c.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
          html += `<td>${formatted}</td>`; 
        });
        html += '</tr>';
      }
    });
    html += '</tbody></table></div>';
    return html;
  }

  function formatMarkdown(text) {
    if (!text) return '';

    // First parse tables
    let processed = parseMarkdownTables(text);

    // Extract table placeholders
    const tablePlaceholders = [];
    processed = processed.replace(/<div class="ai-table-wrap">[\s\S]*?<\/div>/g, (match) => {
      tablePlaceholders.push(match);
      return `__TABLE_PLACEHOLDER_${tablePlaceholders.length - 1}__`;
    });

    let escaped = processed
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // Restore tables
    tablePlaceholders.forEach((tHtml, idx) => {
      escaped = escaped.replace(`__TABLE_PLACEHOLDER_${idx}__`, tHtml);
    });

    // Horizontal divider
    escaped = escaped.replace(/^---$/gim, '<hr class="ai-chat-divider">');

    // Headers
    escaped = escaped.replace(/^### (.*$)/gim, '<h5 class="ai-msg-h5">$1</h5>');
    escaped = escaped.replace(/^## (.*$)/gim, '<h4 class="ai-msg-h4">$1</h4>');

    // Bold & Italics
    escaped = escaped.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');
    escaped = escaped.replace(/\*(.*?)\*/gim, '<em>$1</em>');

    // Bullet points
    escaped = escaped.replace(/^\* (.*$)/gim, '<li class="ai-bullet-item">$1</li>');
    escaped = escaped.replace(/^- (.*$)/gim, '<li class="ai-bullet-item">$1</li>');
    escaped = escaped.replace(/• (.*$)/gim, '<li class="ai-bullet-item">$1</li>');
    escaped = escaped.replace(/(<li class="ai-bullet-item">.*?<\/li>)+/gis, '<ul class="ai-bullet-list">$&</ul>');

    // Convert newlines to paragraphs & breaks
    escaped = escaped.replace(/\n\n/g, '</p><p>');
    escaped = escaped.replace(/\n/g, '<br>');

    // Clickable links
    escaped = escaped.replace(/(\+91\s?\d{10})/g, '<a href="tel:+919919980246" class="ai-chat-link">📞 $1</a>');
    escaped = escaped.replace(/([a-zA-Z0-9._%+-]+@gmail\.com)/gi, '<a href="mailto:$1" class="ai-chat-link">✉️ $1</a>');
    escaped = escaped.replace(/(\/courses\/[a-z0-9\-_]+\/)/gi, '<a href="$1" class="ai-chat-link">🔗 View Program</a>');

    return `<div class="ai-msg-body-content">${escaped}</div>`;
  }

  function appendUserMessage(text) {
    const messagesEl = document.getElementById('ai-chat-messages');
    if (!messagesEl) return;

    const userDiv = document.createElement('div');
    userDiv.className = 'ai-msg-bubble ai-msg-user';
    userDiv.innerHTML = `
      <div class="ai-msg-content">
        <p>${text.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</p>
      </div>
    `;
    messagesEl.appendChild(userDiv);
    scrollToBottom();
  }

  function showTypingIndicator() {
    const messagesEl = document.getElementById('ai-chat-messages');
    if (!messagesEl) return null;

    const typingDiv = document.createElement('div');
    typingDiv.id = 'ai-chat-typing';
    typingDiv.className = 'ai-msg-bubble ai-msg-bot';
    typingDiv.innerHTML = `
      <div class="ai-msg-avatar">
        <span class="ai-avatar-letter">M</span>
        <span class="ai-avatar-spark">✦</span>
      </div>
      <div class="ai-msg-content ai-typing-content">
        <span class="ai-typing-dot"></span>
        <span class="ai-typing-dot"></span>
        <span class="ai-typing-dot"></span>
      </div>
    `;
    messagesEl.appendChild(typingDiv);
    scrollToBottom();
    return typingDiv;
  }

  function removeTypingIndicator() {
    const typing = document.getElementById('ai-chat-typing');
    if (typing) typing.remove();
  }

  function appendBotMessage(replyText) {
    const messagesEl = document.getElementById('ai-chat-messages');
    if (!messagesEl) return;

    const botDiv = document.createElement('div');
    botDiv.className = 'ai-msg-bubble ai-msg-bot';
    botDiv.innerHTML = `
      <div class="ai-msg-avatar">
        <span class="ai-avatar-letter">M</span>
        <span class="ai-avatar-spark">✦</span>
      </div>
      <div class="ai-msg-content">
        ${formatMarkdown(replyText)}
      </div>
    `;
    messagesEl.appendChild(botDiv);
    scrollToBottom();
  }

  function scrollToBottom() {
    const messagesEl = document.getElementById('ai-chat-messages');
    if (messagesEl) {
      setTimeout(() => {
        messagesEl.scrollTop = messagesEl.scrollHeight;
      }, 60);
    }
  }

  async function sendUserMessage(messageText) {
    if (!messageText.trim() || isAwaitingResponse) return;

    appendUserMessage(messageText);

    isAwaitingResponse = true;
    const sendBtn = document.getElementById('ai-chat-send-btn');
    if (sendBtn) sendBtn.disabled = true;

    showTypingIndicator();

    try {
      const csrfToken = getCookie('csrftoken') || '';
      const headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      };
      if (csrfToken) {
        headers['X-CSRFToken'] = csrfToken;
      }

      const response = await fetch('/api/chatbot/', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          message: messageText,
          history: chatHistory.slice(-6)
        })
      });

      removeTypingIndicator();

      const data = await response.json().catch(() => null);

      if (response.ok && data && data.reply) {
        appendBotMessage(data.reply);
        chatHistory.push({ role: 'user', text: messageText });
        chatHistory.push({ role: 'model', text: data.reply });
      } else if (data && data.reply) {
        appendBotMessage(data.reply);
        chatHistory.push({ role: 'user', text: messageText });
        chatHistory.push({ role: 'model', text: data.reply });
      } else {
        const fallbackMsg = "Hello! I am here to guide you on Mayank Classes courses, fee structures, and batch schedules. You can ask about our **NEET** (₹79,000), **JEE** (₹82,000), or **Classes 6–10 Foundation** (starting at ₹27,500) programs. You can also call **+91 9919980246**!";
        appendBotMessage(fallbackMsg);
      }
    } catch (err) {
      removeTypingIndicator();
      console.error('Chatbot request error:', err);
      const fallbackMsg = "Hello! I am here to guide you on Mayank Classes courses, fee structures, and batch schedules. You can ask about our **NEET** (₹79,000), **JEE** (₹82,000), or **Classes 6–10 Foundation** (starting at ₹27,500) programs, or call **+91 9919980246**!";
      appendBotMessage(fallbackMsg);
    } finally {
      isAwaitingResponse = false;
      if (sendBtn) sendBtn.disabled = false;
      const input = document.getElementById('ai-chat-input');
      if (input) input.focus();
    }
  }

  // Auto initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChatbot);
  } else {
    initChatbot();
  }
})();

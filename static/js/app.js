document.addEventListener('DOMContentLoaded', () => {
        const messages = document.getElementById('messages');
  const userInput = document.getElementById('user-input');
  const sendBtn = document.getElementById('send-btn');
  const clearBtn = document.getElementById('clear-btn');
  const chatHelper = document.getElementById('chat-helper');
  const promptBar = document.getElementById('suggested-prompts-bar');

  const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

        const modals = {
    genre: document.getElementById('genre-modal'),
    theme: document.getElementById('theme-modal'),
    avatar: document.getElementById('avatar-modal'),
    detail: document.getElementById('anime-detail-modal')
  };

  function openModal(modal) {
    modal.classList.add('open');
  }

  function closeModal(modal) {
    modal.classList.remove('open');
  }

    document.getElementById('btn-genre').addEventListener('click', () => openModal(modals.genre));
  modals.genre.querySelector('.close').addEventListener('click', () => closeModal(modals.genre));

    document.getElementById('btn-theme').addEventListener('click', () => openModal(modals.theme));
  modals.theme.querySelector('.close').addEventListener('click', () => closeModal(modals.theme));

    document.querySelector('.header-avatar').addEventListener('click', () => openModal(modals.avatar));
  document.getElementById('close-modal').addEventListener('click', () => closeModal(modals.avatar));

    document.querySelector('.anime-detail-close').addEventListener('click', () => closeModal(modals.detail));

    Object.values(modals).forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal(modal);
    });
  });

        function typeText(element, htmlText, speed = 15) {
    return new Promise((resolve) => {
      let displayHTML = '';
      let charIndex = 0;
      const fullHTML = htmlText;

      function addChar() {
        if (charIndex < fullHTML.length) {
          displayHTML += fullHTML[charIndex];
          element.innerHTML = displayHTML;
          charIndex++;
          setTimeout(addChar, speed);
        } else {
          element.innerHTML = fullHTML;
          resolve();
        }
      }

      addChar();
    });
  }

        async function sendMessage() {
    const msg = userInput.value.trim();
    if (!msg) return;

    if (isMobile) userInput.blur();

    chatHelper.style.display = 'none';
    promptBar.classList.add('hidden');

        const userMsg = document.createElement('div');
    userMsg.className = 'chat-message user';
    userMsg.textContent = msg;
    messages.appendChild(userMsg);

    userInput.value = '';
    sendBtn.disabled = true;
    sendBtn.classList.add('loading');
    userInput.disabled = true;

    setTimeout(() => {
      const chatArea = document.querySelector('.chat-area');
      chatArea.scrollTop = chatArea.scrollHeight;
    }, 100);

        const typing = document.createElement('div');
    typing.className = 'typing';
    typing.innerHTML = '<span></span><span></span><span></span>';
    messages.appendChild(typing);

    setTimeout(() => {
      const chatArea = document.querySelector('.chat-area');
      chatArea.scrollTop = chatArea.scrollHeight;
    }, 100);

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
      });

      const data = await response.json();
      typing.remove();

      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = data.reply;
      const animeCards = tempDiv.querySelectorAll('.anime-card');

      const botMsg = document.createElement('div');
      botMsg.className = 'chat-message bot';
      messages.appendChild(botMsg);

      if (animeCards.length > 0) {
                let introHTML = '';
        let node = tempDiv.firstChild;
        while (node && node !== animeCards[0]) {
          if (node.nodeType === Node.TEXT_NODE) {
            introHTML += node.textContent;
          } else if (node.nodeType === Node.ELEMENT_NODE) {
            introHTML += node.outerHTML;
          }
          node = node.nextSibling;
        }
        introHTML = introHTML.trim();

        if (introHTML) {
          await typeText(botMsg, introHTML);
          botMsg.appendChild(document.createElement('br'));
          botMsg.appendChild(document.createElement('br'));

          const chatArea = document.querySelector('.chat-area');
          chatArea.scrollTop = chatArea.scrollHeight;
        }

                for (const card of animeCards) {
          const clonedCard = card.cloneNode(true);
          clonedCard.style.opacity = '0';
          clonedCard.style.animation = 'fadeIn 0.5s ease forwards';
          botMsg.appendChild(clonedCard);
          await new Promise(resolve => setTimeout(resolve, 150));

          const chatArea = document.querySelector('.chat-area');
          chatArea.scrollTop = chatArea.scrollHeight;
        }

                let footerHTML = '';
        let footerNode = animeCards[animeCards.length - 1].nextSibling;
        while (footerNode) {
          if (footerNode.nodeType === Node.TEXT_NODE) {
            footerHTML += footerNode.textContent;
          } else if (footerNode.nodeType === Node.ELEMENT_NODE) {
            footerHTML += footerNode.outerHTML;
          }
          footerNode = footerNode.nextSibling;
        }
        footerHTML = footerHTML.trim();

        if (footerHTML) {
          botMsg.appendChild(document.createElement('br'));
          const footerDiv = document.createElement('div');
          botMsg.appendChild(footerDiv);
          await typeText(footerDiv, footerHTML);

          const chatArea = document.querySelector('.chat-area');
          chatArea.scrollTop = chatArea.scrollHeight;
        }

        attachDetailButtons();
      } else {
        await typeText(botMsg, tempDiv.innerHTML.trim());

        const chatArea = document.querySelector('.chat-area');
        chatArea.scrollTop = chatArea.scrollHeight;
      }

      const chatArea = document.querySelector('.chat-area');
      chatArea.scrollTop = chatArea.scrollHeight;

    } catch (error) {
      typing.remove();
      const errorMsg = document.createElement('div');
      errorMsg.className = 'chat-message bot';
      errorMsg.textContent = '⚠️ Gagal terhubung ke server';
      messages.appendChild(errorMsg);

      const chatArea = document.querySelector('.chat-area');
      chatArea.scrollTop = chatArea.scrollHeight;
    } finally {
      sendBtn.disabled = false;
      sendBtn.classList.remove('loading');
      userInput.disabled = false;
      if (!isMobile) userInput.focus();
    }
  }

  sendBtn.addEventListener('click', sendMessage);
  userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    }
  });

        function attachDetailButtons() {
    document.querySelectorAll('.detail-btn:not([data-listener])').forEach(btn => {
      btn.addEventListener('click', function () {
        const dataStr = this.getAttribute('data-anime');
        if (!dataStr) return;

        const data = JSON.parse(dataStr.replace(/&quot;/g, '"'));

        document.getElementById('detail-name').textContent = data.name || 'Tidak tersedia';
        document.getElementById('detail-english-name').textContent = data.english_name || 'Tidak tersedia';
        document.getElementById('detail-genres').textContent = data.genres || 'Tidak ada';
        document.getElementById('detail-themes').textContent = data.themes || 'Tidak ada';
        document.getElementById('detail-score').textContent = data.score || 'Tidak tersedia';
        document.getElementById('detail-episodes').textContent = data.episodes || 'Tidak tersedia';
        document.getElementById('detail-duration').textContent = data.duration || 'Tidak tersedia';
        document.getElementById('detail-premiered').textContent = data.premiered || 'Tidak tersedia';
        document.getElementById('detail-synopsis').textContent = data.synopsis || 'Sinopsis tidak tersedia';
        document.getElementById('detail-image').src = data.image_url || '';
        document.getElementById('detail-mal-link').href = data.anime_url || '#';

        openModal(modals.detail);
      });

      btn.dataset.listener = 'true';
    });
  }

        clearBtn.addEventListener('click', () => {
    if (confirm('Yakin ingin menghapus semua chat?\nHalaman akan dimuat ulang dan semua chat akan terhapus')) {
      window.location.reload();
    }
  });

        document.querySelectorAll('.prompt-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      userInput.value = chip.getAttribute('data-prompt');
      sendMessage();
    });
  });

        userInput.focus();

  if (!isMobile) {
    document.addEventListener('keydown', (e) => {
      if (document.activeElement === userInput) return;

      const modalOpen = Object.values(modals).some(m => m.classList.contains('open'));
      if (modalOpen) return;

      if (e.ctrlKey || e.altKey || e.metaKey || e.key === 'Tab' || e.key === 'Escape') return;

      if (e.key.length === 1) {
        userInput.focus();
      }
    });
  }

        if (isMobile && window.visualViewport) {
    const inputBar = document.querySelector('.input-bar');
    const chatArea = document.querySelector('.chat-area');

    function adjustForKeyboard() {
      const vv = window.visualViewport;
      const offset = window.innerHeight - vv.height - vv.offsetTop;

      if (offset > 0) {
        inputBar.style.transform = `translate(-50%, -${offset}px)`;
        chatArea.style.paddingBottom = `${offset + inputBar.offsetHeight + 20}px`;
      } else {
        inputBar.style.transform = 'translate(-50%, 0)';
        chatArea.style.paddingBottom = `${inputBar.offsetHeight + 20}px`;
      }
    }

    visualViewport.addEventListener('resize', adjustForKeyboard);
    visualViewport.addEventListener('scroll', adjustForKeyboard);
    adjustForKeyboard();
  }
        window.copyTextUniversal = function (btn, text) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text)
        .then(() => showCopySuccess(btn))
        .catch(() => fallbackCopy(btn, text));
    } else {
            fallbackCopy(btn, text);
    }
  };

  function fallbackCopy(btn, text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.top = '0';
    textarea.style.left = '-9999px';
    textarea.setAttribute('readonly', '');

    document.body.appendChild(textarea);

        if (navigator.userAgent.match(/ipad|iphone/i)) {
      const range = document.createRange();
      range.selectNodeContents(textarea);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      textarea.setSelectionRange(0, 999999);
    } else {
      textarea.select();
    }

    try {
      const success = document.execCommand('copy');
      if (success) {
        showCopySuccess(btn);
      }
    } catch (err) {
      console.error('Copy failed:', err);
    }

    document.body.removeChild(textarea);
  }

  function showCopySuccess(btn) {
    const original = btn.innerHTML;
    btn.innerHTML = '✓';
    btn.classList.add('copied');

    setTimeout(() => {
      btn.innerHTML = original;
      btn.classList.remove('copied');
    }, 1500);
  }
});

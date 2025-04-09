const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

registerBtn.addEventListener('click', () => {
  container.classList.add('active');
});

loginBtn.addEventListener('click', () => {
  container.classList.remove('active');
});

// SEND CODE BUTTON HANDLER
const sendCodeBtn = document.getElementById('send-code-btn');
sendCodeBtn?.addEventListener('click', async () => {
  const form = document.getElementById('login-form');
  const formData = new FormData(form);
  const username = formData.get('username');
  const password = formData.get('password');
  const codeStatus = document.getElementById('code-status');

  if (!username || !password) {
    codeStatus.style.color = 'red';
    codeStatus.innerText = 'Enter username and password first.';
    return;
  }

  const response = await fetch('/users/authenticate/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      action: 'send_2fa_code',
      username,
      password
    })
  });

  const result = await response.json();
  codeStatus.style.color = result.success ? 'green' : 'red';
  codeStatus.innerText = result.success ? 'Code sent! Check console.' : result.error;
});

document.querySelectorAll('.auth-form').forEach(form => {
  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const action = this.dataset.action;
    const formData = new FormData(this);
    const data = { action };

    formData.forEach((value, key) => {
      data[key] = value;
    });

    if (action === 'login' && data.code?.trim()) {
      data.action = 'verify_2fa';
    }

    const response = await fetch('/users/authenticate/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    const errorBox = this.querySelector('.error-box');

    if (result.success) {
      window.location.href = '/';
    } else {
      if (errorBox) {
        errorBox.innerText = result.error;
        errorBox.style.display = 'block';
      } else {
        const box = document.createElement('div');
        box.className = 'error-box';
        box.style.color = 'red';
        box.style.marginBottom = '10px';
        box.innerText = result.error;
        this.prepend(box);
      }
    }
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

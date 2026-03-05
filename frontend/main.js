const API_BASE = 'http://localhost:3005/api';

let currentUser = localStorage.getItem('ctf_username') || '';

document.addEventListener('DOMContentLoaded', () => {
    if (currentUser) {
        showDashboard();
    }

    document.getElementById('login-btn').addEventListener('click', () => {
        const username = document.getElementById('username-input').value.trim();
        if (username) {
            currentUser = username;
            localStorage.setItem('ctf_username', username);
            showDashboard();
        }
    });

    // Subtly track mouse on cards
    document.querySelectorAll('.challenge-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(0, 255, 65, 0.05) 0%, var(--bg-secondary) 50%)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.background = 'var(--bg-secondary)';
        });
    });
});

function showDashboard() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('dashboard-section').style.display = 'block';
    document.getElementById('current-user').innerText = currentUser;
    loadLeaderboard();
}

async function loadLeaderboard() {
    try {
        const res = await fetch(`${API_BASE}/leaderboard`);
        const data = await res.json();
        const list = document.getElementById('leaderboard-list');
        list.innerHTML = '';

        if (data.length === 0) {
            list.innerHTML = '<li>No hackers yet. Be the first!</li>';
            return;
        }

        data.forEach((user, index) => {
            const li = document.createElement('li');
            li.innerHTML = `<span>${index + 1}. ${user.username}</span> <span>${user.score} pts</span>`;
            if (user.username === currentUser) {
                li.style.color = 'var(--primary-color)';
                li.style.fontWeight = 'bold';
            }
            list.appendChild(li);
        });
    } catch (e) {
        console.error("Failed to load leaderboard");
    }
}

window.submitFlag = async function (challengeId) {
    const flagInput = document.getElementById(`flag-${challengeId}`);
    const statusDiv = document.getElementById(`status-${challengeId}`);
    const flag = flagInput.value.trim();

    if (!flag) {
        statusDiv.innerText = "Please enter a flag.";
        statusDiv.className = "status-msg error";
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: currentUser, challengeId, flag })
        });

        const data = await res.json();

        if (res.ok && data.success) {
            statusDiv.innerText = data.message;
            statusDiv.className = "status-msg success";
            flagInput.value = '';
            loadLeaderboard();
        } else if (res.status === 429) {
            statusDiv.innerText = data.error;
            statusDiv.className = "status-msg error";
        } else {
            statusDiv.innerText = data.message || data.error;
            statusDiv.className = "status-msg error";
        }
    } catch (e) {
        statusDiv.innerText = "Network Error.";
        statusDiv.className = "status-msg error";
    }
};

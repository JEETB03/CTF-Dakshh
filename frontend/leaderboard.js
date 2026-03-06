const API_BASE = 'http://localhost:3005/api';

document.addEventListener('DOMContentLoaded', () => {
    loadFullLeaderboard();
});

async function loadFullLeaderboard() {
    try {
        const currentUser = localStorage.getItem('ctf_username') || '';
        const res = await fetch(`${API_BASE}/leaderboard/full`);
        const data = await res.json();
        const tbody = document.getElementById('full-leaderboard-list');
        tbody.innerHTML = '';

        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">No flags submitted yet.</td></tr>';
            return;
        }

        data.forEach((user, index) => {
            const tr = document.createElement('tr');

            // Check if this row is the current user
            if (user.username === currentUser) {
                tr.className = 'current-user-row';
            }

            tr.innerHTML = `
                <td class="rank">#${index + 1}</td>
                <td>${user.username}</td>
                <td>${user.solved_count}</td>
                <td>${user.score} pts</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error("Failed to load full leaderboard");
        document.getElementById('full-leaderboard-list').innerHTML = '<tr><td colspan="4" style="text-align: center; color: red;">Error connecting to server.</td></tr>';
    }
}

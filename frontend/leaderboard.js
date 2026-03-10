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

        if (!data.leaderboard || data.leaderboard.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">No flags submitted yet.</td></tr>';
            return;
        }

        data.leaderboard.forEach((user, index) => {
            const tr = document.createElement('tr');

            // Check if this row is the current user
            if (user.username === currentUser) {
                tr.className = 'current-user-row';
            }

            // Safe DOM insertion to prevent Stored XSS
            const tdRank = document.createElement('td');
            tdRank.className = 'rank';
            tdRank.textContent = `#${index + 1}`;

            const tdUsername = document.createElement('td');
            tdUsername.textContent = user.username;

            const tdSolved = document.createElement('td');
            tdSolved.textContent = `${user.solved_count} / ${data.totalChallenges}`;

            const tdScore = document.createElement('td');
            tdScore.textContent = `${user.score} pts`;

            tr.appendChild(tdRank);
            tr.appendChild(tdUsername);
            tr.appendChild(tdSolved);
            tr.appendChild(tdScore);

            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error("Failed to load full leaderboard");
        document.getElementById('full-leaderboard-list').innerHTML = '<tr><td colspan="4" style="text-align: center; color: red;">Error connecting to server.</td></tr>';
    }
}

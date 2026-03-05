document.addEventListener('DOMContentLoaded', () => {
    const loginContainer = document.getElementById('login-container');
    const dashboardContainer = document.getElementById('dashboard-container');
    const loginForm = document.getElementById('login-form');
    const loginError = document.getElementById('login-error');

    // Auth State
    let currentUser = null;

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const empId = document.getElementById('emp-id').value;
        const pwd = document.getElementById('password').value; // In a secure system, this matters...

        // Vulnerability: No real auth check, we just fetch the user profile API endpoint directly
        try {
            const res = await fetch(`/api/v1/user?id=${empId}`);
            const data = await res.json();

            if (data.success) {
                currentUser = { id: empId, ...data.data };
                loginContainer.style.display = 'none';
                dashboardContainer.style.display = 'flex';
                loadDashboard();
            } else {
                loginError.style.display = 'block';
                loginError.innerText = "Authentication failed. Invalid ID.";
            }
        } catch (err) {
            loginError.style.display = 'block';
            loginError.innerText = "System offline.";
        }
    });

    document.getElementById('logout-btn').addEventListener('click', () => {
        currentUser = null;
        dashboardContainer.style.display = 'none';
        loginContainer.style.display = 'flex';
        document.getElementById('docs-body').innerHTML = '<tr><td colspan="3" class="loading">Loading records...</td></tr>';
    });

    async function loadDashboard() {
        document.getElementById('nav-user-name').innerText = currentUser.name;
        document.getElementById('nav-user-avatar').innerText = currentUser.name[0];
        document.getElementById('welcome-text').innerText = `Welcome back, ${currentUser.name.split(' ')[0]}`;

        document.getElementById('profile-name').innerText = currentUser.name;
        document.getElementById('profile-dept').innerText = currentUser.dept;
        document.getElementById('profile-avatar').innerText = currentUser.name[0];

        // Fetch user documents using the vulnerable API
        loadDocuments();
    }

    async function loadDocuments() {
        const docsBody = document.getElementById('docs-body');
        try {
            const res = await fetch(`/api/v1/documents?user_id=${currentUser.id}`);
            const data = await res.json();

            if (data.success) {
                docsBody.innerHTML = '';
                if (data.data.length === 0) {
                    docsBody.innerHTML = '<tr><td colspan="3" class="loading">No authorization for document access.</td></tr>';
                    return;
                }

                data.data.forEach(doc => {
                    const tr = document.createElement('tr');

                    const tdName = document.createElement('td');
                    tdName.innerText = doc.name;
                    if (doc.restricted) {
                        const span = document.createElement('span');
                        span.className = 'restricted-label';
                        span.innerText = 'RESTRICTED';
                        tdName.appendChild(span);
                    }

                    const tdClearance = document.createElement('td');
                    tdClearance.innerText = doc.restricted ? 'Executive Level' : 'Standard';

                    const tdAction = document.createElement('td');
                    const btn = document.createElement('a');
                    btn.className = 'download-link';
                    btn.href = `/api/v1/download?file=${doc.filename}`;
                    btn.innerText = 'Download';
                    btn.setAttribute('download', '');
                    tdAction.appendChild(btn);

                    tr.appendChild(tdName);
                    tr.appendChild(tdClearance);
                    tr.appendChild(tdAction);

                    docsBody.appendChild(tr);
                });
            } else {
                docsBody.innerHTML = '<tr><td colspan="3" class="loading">Failed to load records.</td></tr>';
            }
        } catch (err) {
            docsBody.innerHTML = '<tr><td colspan="3" class="loading">Database connection error.</td></tr>';
        }
    }
});

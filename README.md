# GitHub Webhook Receiver (Flask + MongoDB Atlas)

This project is built as part of a **Developer Assessment Task**.

It demonstrates how GitHub webhook events (**Push**, **Pull Request**, **Merge**) can be received by a backend service, stored in a database, and displayed on a simple UI that updates automatically every **15 seconds**.

---

## Repositories

- **Action Repository (Event Source)**  
  https://github.com/nsnavneet/action-repo  

- **Webhook Repository (Backend + UI)**  
  https://github.com/nsnavneet/webhook-repo  

---

## What This Project Does

1. GitHub events occur in the **action-repo**
   - Push commits
   - Create pull requests
   - Merge pull requests

2. GitHub sends webhook payloads to a Flask backend endpoint:
POST /webhook


3. The Flask server:
- Receives webhook payloads
- Identifies the event type
- Extracts required fields
- Stores the data in MongoDB Atlas

4. A simple frontend UI:
- Polls the backend every **15 seconds**
- Displays GitHub activity in a human-readable format

---

## Tech Stack

- Backend: Python, Flask  
- Database: MongoDB Atlas (Cloud)  
- Webhook Tunneling: ngrok  
- Frontend: HTML, CSS, JavaScript  
- Version Control: Git & GitHub  

---

## MongoDB Schema

**Database Name**
github_events


**Collection Name**
events


Each document contains:
- request_id
- author
- action (PUSH | PULL_REQUEST | MERGE)
- from_branch
- to_branch
- timestamp

---

## UI Output Format

**Push Event**
{author} pushed to {to_branch} on {timestamp}


**Pull Request Event**
{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}


**Merge Event**
{author} merged branch {from_branch} to {to_branch} on {timestamp}


The UI refreshes automatically every **15 seconds**.

---

## Setup & Installation

### 1. Clone the Repository
bash
git clone https://github.com/nsnavneet/webhook-repo.git
cd webhook-repo

2. Create Virtual Environment & Install Dependencies
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
3. Create Environment File
Create a .env file in the project root:

MONGO_URI=<your_mongodb_atlas_connection_string>
MONGO_DB=github_events
MONGO_COLLECTION=events
Notes

.env is ignored using .gitignore

Sensitive credentials are not committed to GitHub

4. Run the Flask Application
python app.py
Server will start at:

http://localhost:5000
5. Expose Webhook Endpoint Using ngrok
ngrok http 5000
Example public URL:

https://xxxx.ngrok-free.app
GitHub Webhook Configuration (action-repo)
Go to:

Settings → Webhooks → Add webhook
Configure:

Payload URL

https://<ngrok-url>/webhook
Content type: application/json

Events

Pushes

Pull requests

Save the webhook.

Testing the System
Push Event
git commit -m "test push"
git push
Pull Request Event
Create a new branch

Push changes

Open a Pull Request on GitHub

Merge Event
Merge the Pull Request into main

All events will appear automatically on the UI.

View the UI
Open in browser:

http://localhost:5000
The UI fetches and displays GitHub events every 15 seconds.

Project Structure
webhook-repo/
│
├── app.py
├── requirements.txt
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── styles.css
└── README.md
Final Status
Push events captured successfully

Pull request events captured successfully

Merge events captured successfully

Data stored in MongoDB Atlas

UI auto-refresh working every 15 seconds

Author
Navneet Singh
GitHub: https://github.com/nsnavneet

Final Step
git add README.md
git commit -m "add final README"
git push

---

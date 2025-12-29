# Studify

A study tracking application built with a **Cloud-First** architecture. This project helps users manage subjects, track study hours in real-time, earn points, and connect with friends.

## 🏗 Architecture Overview

This project leverages a decoupled architecture to ensure scalability and ease of deployment.

* **Frontend:** Vanilla HTML5, CSS3, and JavaScript (ES6).
* **Backend:** Flask (Python) REST API.
* **Database:** Azure SQL Database (Serverless tier).
* **Deployment:** CI/CD via GitHub Actions to Azure App Service.

## 🗄 Database Design

A relational schema to handle complex user interactions.

* **Schema:** 5 Core Tables (`users`, `subjects`, `tasks`, `study_logs`, `friends`).
* **Key Logic:**
* **Normalization:** Tasks are categorized by subjects.
* **Integrity:** Implemented a unique constraint on the `friends` table `(user_id1 < user_id2)` to prevent duplicate relationship rows.
* **Performance:** Utilized Azure SQL Serverless (0.5–2 vCores) to balance cost and performance for a student budget.



## 🛠 Integration & QA Challenges

The most significant phase of this project was the **"Connection Gap"**: ensuring the frontend and backend communicated perfectly with the cloud database.

* **Log Streaming:** Used **Azure Log Stream** to debug real-time API failures and connection string issues.
* **QA Testing:** Performing end-to-end testing on the point reward system (1 point per 10 minutes of logged study time) and the friend request lifecycle.

## 👥 The Team
This project was a collaborative effort, and the synergy within the team is what turned a complex cloud migration into a success.

**Marev Wasim (DBA & QA Lead)**: Database architecture, Azure configuration, and system integration.

**Shahd Khalil (Backend Dev)**: Flask API development and business logic.

**Omnia Mansour (UI/UX Designer)**:	Project's visual identity and client-side logic.

**Mohraiel Emad (Frontend Dev)**: Interactive logic of the website and frontend with the backend integration.

## 🚀 Local Setup

1. Clone the repo: `git clone [URL]`
2. Install dependencies: `pip install -r requirements.txt`
3. **Environment Variables:** Create a `.env` file with your Azure SQL Connection String:
```bash
DB_CONNECTION_STRING="Driver={ODBC Driver 18 for SQL Server};Server=..."

```


4. Run the app: `python app.py`

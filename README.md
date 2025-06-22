# 🤖 EaseAgent Backend

A smart FastAPI backend for managing email replies, meeting scheduling, and intelligent agent coordination using Google Gemini AI.

---

## 🚀 Project Overview

EaseAgent is an AI assistant system designed to automate tasks for small businesses. This backend provides core functionality including:

- ✉️ Email sending and reply generation
- 📅 Meeting booking and time suggestion
- 🧠 Natural language parsing of meeting requests (via Gemini)
- 🧠 Multi-agent system structure with capabilities per agent

---

## 🛠️ Tech Stack

- **FastAPI** – High-performance web framework
- **Pydantic** – Data validation and typing
- **Google Gemini Pro Vision** – For AI text generation
- **Python 3.11+**
- **dotenv** – For managing environment variables

---

## 📁 Project Structure

## 📁 Project Structure

<pre>
backend/
├── APP/
│   ├── agents/
│   │   ├── email_agent.py
│   │   ├── meeting_agent.py
│   │   └── task_agent.py
│   ├── routes/
│   │   ├── email.py
│   │   ├── meetings.py
│   │   ├── task.py
│   │   └── agent.py
│   ├── schemas/
│   │   ├── email.py
│   │   ├── meeting.py
│   │   ├── reply_request.py
│   │   └── ...
│   ├── utils/
│   │   └── gemini_connector.py
│   └── main.py
├── meetings.json
├── business_profiles.json
├── .env
└── README.md
</pre>

---

## 🔑 Environment Setup

Create a `.env` file in the root (`backend/`) with:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
📦 Installation
bash
Copy
Edit
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt
▶️ Run the Server
bash
Copy
Edit
uvicorn APP.main:app --reload
Then open http://127.0.0.1:8000/docs for Swagger API documentation.

🧠 AI Features (Gemini)
1. Generate Email Reply
http
Copy
Edit
POST /emails/reply
{
  "email_text": "Hey, can we meet tomorrow to discuss the EaseAgent prototype?"
}
✅ Returns a polite, professional AI-generated reply.

2. Parse Meeting Request (NLP)
http
Copy
Edit
POST /meetings/parse-request
{
  "message": "Are you free tomorrow at 3 PM to talk about EaseAgent?"
}
✅ Extracts structured JSON:

json
Copy
Edit
{
  "date": "2025-06-22",
  "time": "15:00",
  "topic": "EaseAgent discussion",
  "email": null
}
📅 Meeting Booking Features
Get Available Slot
http
Copy
Edit
GET /meetings/{email}/{date}
Returns suggested next available slot for that user.

Book a Meeting
http
Copy
Edit
POST /meetings/
{
  "email": "ankitofficial0425@gmail.com",
  "date": "2025-06-22",
  "time": "11:30",
  "topic": "EaseAgent planning"
}
🧩 Agent System API
Endpoint	Description
GET /agents/	List all agents
POST /agents/	Add a new agent
PUT /agents/{id}	Update agent
DELETE /agents/{id}	Delete agent
POST /agents/email-reply	Generate reply (Gemini)

✅ TODOs / Future Scope
🔒 Add authentication

📊 Analytics dashboard

🧠 Multi-agent orchestration logic

🌐 Frontend integration

👨‍💻 Author
Ankit
B.Tech CSE @ Chandigarh University
Passionate about AI, automation, and building real-world GenAI systems.

🏁 License
This project is for educational and prototype purposes only. Use with proper attribution and API usage limits in mind.

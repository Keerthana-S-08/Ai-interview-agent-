# Ai-interview-agent-
AI Interview Agent is an AI-powered platform that delivers personalized mock interviews with real-time conversations, intelligent follow-ups, and instant feedback. It helps students and professionals practice technical concepts across AI/ML  concepts identify knowledge gaps, and build confidence to perform better in real job interviews anytime.

🤖 AI Interview Agent

<img width="1345" height="642" alt="ab1" src="https://github.com/user-attachments/assets/0466ba05-ed63-449f-aa91-adc93936175d" />







«Build an interviewer, not an interview.»

An AI-powered technical interviewer that conducts personalized, multi-turn interviews based on a candidate's learning journey.

Built for ABTalks Vibe Code Hackathon — Problem Statement 2: The Interview Agent.

---

🎯 The Idea

Traditional interviews ask the same questions to everyone.

AI Interview Agent is different.

Candidate Profile
       ↓
Learning Journey
       ↓
Relevant Technical Question
       ↓
Candidate Answer
       ↓
AI Evaluation
       ↓
Adaptive Follow-up
       ↓
Final Feedback

The interviewer listens, adapts, and remembers the conversation.

---

✨ Key Features

- 🧑‍💻 Personalized Interviews — Questions based on the candidate's completed learning journey.
- 🧠 Curriculum-Aware — Uses the provided 31-day AI curriculum.
- 🔄 Adaptive Questions — Follow-ups change based on previous answers.
- 💬 Multi-Turn Conversation — Maintains context throughout the interview.
- 📊 Technical Evaluation — Understands strong, mixed, and weak responses.
- 📝 Actionable Feedback — Provides summary, strengths, gaps, and next steps.
- 🔌 API-Based — Implements the required "POST /api/interview" endpoint.

---

🏗️ Tech Stack

Layer| Technology
Frontend| React + Vite
Backend| Python + FastAPI
AI| Gemini
Data| JSON
Development| VS Code + GitHub

---

🔄 How It Works

1️⃣ Select Candidate

<img width="1343" height="612" alt="ab2" src="https://github.com/user-attachments/assets/88d776a8-7701-4b9a-9307-4b1455527030" />








<img width="1344" height="629" alt="ab3" src="https://github.com/user-attachments/assets/49dc24f1-5e3d-4f96-ba5d-8c1af70ec069" />


The system loads the candidate's profile and learning history.

2️⃣ Start Interview

<img width="1349" height="635" alt="ab4" src="https://github.com/user-attachments/assets/83f440fc-2dae-4792-8016-6bfb8284d12f" />




The AI selects relevant topics from the curriculum.

3️⃣ Answer

<img width="1348" height="646" alt="ab5" src="https://github.com/user-attachments/assets/b57f73f7-dda7-4acd-9e4a-d8f2365cf844" />


The candidate responds to the technical question.

4️⃣ Adapt

<img width="1349" height="640" alt="ab8" src="https://github.com/user-attachments/assets/333f0cd3-7215-4f27-b4be-eaec7dc10fbf" />






<img width="1345" height="637" alt="ab9" src="https://github.com/user-attachments/assets/b1e6d052-5c0c-4d84-b07c-9219b63e19c7" />


The AI evaluates the answer and generates an intelligent follow-up.

5️⃣ Complete

After the required interview questions, the AI generates a technical report.
<img width="1342" height="687" alt="ab10" src="https://github.com/user-attachments/assets/26974ae1-1b4d-408a-95aa-2adb075ad99d" />


Question → Answer → Evaluate → Adapt → Repeat → Feedback



---

💡 Example

AI:
Explain how RAG works.

Candidate:
RAG retrieves relevant information and provides it to the language model as context.

AI:
Good. How would you evaluate whether your retrieval system is returning relevant documents?

➡️ The next question depends on the previous answer.

---

📊 Final Feedback

At the end of the interview, the candidate receives:

📋 Summary
💪 Strengths
⚠️ Gaps
🚀 Next Steps

The goal is not just to score the candidate, but to help them understand what to improve next.

---

🔌 API

POST /api/interview

The same "sessionId" maintains the conversation across multiple turns.

Start Interview
      ↓
sessionId
      ↓
Question + Answer
      ↓
Same sessionId
      ↓
Adaptive Follow-up

---

📁 Project Structure

ai-interview-agent/
│
├── backend/
│   ├── app/
│   └── data/
│
├── frontend/
│   ├── src/
│   └── public/
│
├── PROMPTS.md
├── README.md
└── .gitignore

---

🚀 Run Locally
<img width="1366" height="729" alt="setup" src="https://github.com/user-attachments/assets/6046782d-0246-42ba-8453-9e7356384909" />

Commands to run the code in VS code.

terminal 1 Backend

cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

terminal 2 Frontend

cd frontend
npm install
npm run dev

Add your Gemini API key to:

backend/.env

---

🧪 Core Requirements

✅ Conversational interview
✅ Minimum 8 questions
✅ 4+ curriculum days
✅ Candidate personalization
✅ Adaptive follow-up questions
✅ Conversation context
✅ Structured final feedback
✅ Required API endpoint

---

🤖 AI-Assisted Development

This project was developed using ChatGPT as the primary AI-assisted development tool for planning, coding assistance, debugging, testing, UI development, and documentation.

Detailed AI usage is documented in:

"PROMPTS.md"

---

🏆 Hackathon

ABTalks Vibe Code Hackathon

Problem Statement 2 — The Interview Agent

«Don't build a questionnaire. Build an interviewer.»

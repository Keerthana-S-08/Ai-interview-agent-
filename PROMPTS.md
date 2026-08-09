# AI Usage Log

This file is intentionally a template. During the hackathon, record the prompts you actually use with AI tools.

Recommended format:

AI Usage Log — AI Interview Agent

Hackathon

ABTalks Vibe Code Hackathon

Selected Problem Statement

Problem Statement 2 — The Interview Agent

---

1. AI Development Assistant

Primary AI tool used: ChatGPT

ChatGPT was used throughout the development of this project as an AI-assisted development and problem-solving tool.

The AI was used for:

- Understanding the problem statement and technical requirements
- Planning the application architecture
- Designing the frontend and backend structure
- Generating and improving code
- Working with the provided curriculum and candidate data
- Designing the interview flow
- Implementing adaptive questioning
- Implementing candidate-specific interview logic
- Designing the API contract
- Debugging and troubleshooting
- Testing edge cases
- Improving the user interface
- Preparing project documentation
- Reviewing the project against the hackathon requirements

The final implementation was reviewed, tested, and adjusted during development rather than being accepted blindly from AI-generated output.

---

2. Understanding the Problem

Prompt / Development Goal

«Analyze the ABTalks Problem Statement 2 and explain the complete requirements for building the AI Interview Agent, including the minimum number of questions, curriculum coverage, candidate personalization, adaptive follow-up questions, conversation context, final feedback, and API requirements.»

AI Assistance

ChatGPT helped break the problem statement into the following major requirements:

1. Conduct a conversational technical interview.
2. Ask at least 8 questions.
3. Cover at least 4 different curriculum days.
4. Personalize questions using the candidate's learning journey.
5. Generate intelligent follow-up questions.
6. Maintain conversation context.
7. Evaluate candidate responses.
8. Generate structured final feedback.
9. Implement the required HTTP API endpoint.
10. Follow the supplied technical specification.

---

3. Understanding the Official Resources

The hackathon provided three important resources:

- Curriculum JSON
- Candidate Profiles
- Technical Specification

Prompt / Development Goal

«Analyze the official curriculum, candidate profiles, and technical specification and explain how they should be used in the AI Interview Agent.»

AI Assistance

ChatGPT helped determine how the supplied resources should be integrated into the application.

The curriculum is used as the source of:

- Modules
- Daily topics
- Learning objectives
- Tools
- Technical concepts

Candidate profiles are used to determine:

- Completed missions
- Attempts
- Skipped topics
- Learning signals
- Candidate-specific interview scope

The Technical Specification is used to implement the required request and response format for the interview endpoint.

The provided resources are treated as the source of truth for the project.

---

4. Project Architecture

Prompt / Development Goal

«Design a practical frontend and backend architecture for the AI Interview Agent that can run locally in VS Code and later be deployed for the hackathon.»

AI Assistance

ChatGPT helped design the following architecture:

React Frontend
      |
      | HTTP Request
      v
FastAPI Backend
      |
      +----------------+
      |                |
      v                v
Candidate Data     Curriculum Data
      |                |
      +--------+-------+
               |
               v
       Interview Engine
               |
               v
            LLM
               |
               v
       Session State
               |
               v
     Final Interview Feedback

The architecture separates the user interface, API layer, interview logic, supplied data, and AI reasoning.

---

5. Candidate Personalization

Prompt / Development Goal

«Make the technical interview personalized to the candidate's actual learning journey instead of asking the same questions to every candidate.»

AI Assistance

ChatGPT helped design logic that considers the candidate's completed learning missions.

The interviewer uses the candidate's completed topics to select appropriate curriculum areas.

This allows different candidates to receive different interview questions based on their learning journey.

For example, if a candidate has completed topics related to:

- RAG
- Vector Databases
- Prompt Engineering
- MCP

the interviewer can focus questions around those areas.

The system avoids treating every candidate as if they completed the same curriculum.

---

6. Adaptive Interviewing

Prompt / Development Goal

«Build an interviewer that behaves like a real technical interviewer instead of asking a fixed list of questions.»

AI Assistance

ChatGPT helped design an adaptive interview flow.

The system considers the candidate's previous response before generating the next question.

A strong response can lead to a deeper technical question.

A weak or incomplete response can lead to:

- Clarification
- A simpler conceptual question
- A follow-up question testing the same concept

This creates a multi-turn interview instead of a static questionnaire.

---

7. Conversation Context

Prompt / Development Goal

«Maintain the context of the interview across multiple API requests using a session ID.»

AI Assistance

ChatGPT helped design session-based state management.

The session stores information such as:

Session ID
Candidate
Conversation history
Questions asked
Answers received
Covered curriculum days
Response evaluations
Current interview progress

The same "sessionId" is used throughout the interview so the backend can understand previous answers and maintain continuity.

---

8. Minimum Interview Requirements

Prompt / Development Goal

«Ensure that the implementation satisfies the requirement of at least 8 questions covering at least 4 curriculum days.»

AI Assistance

ChatGPT helped implement interview progress tracking.

The system tracks:

Question count
Covered curriculum days
Interview history

The interview continues until the required minimum number of questions has been completed while maintaining curriculum coverage.

The goal is to prevent the application from simply asking eight unrelated questions.

---

9. Interview Evaluation

Prompt / Development Goal

«Evaluate candidate answers so that the next question can adapt to the candidate's performance.»

AI Assistance

ChatGPT helped design response evaluation categories such as:

Strong
Mixed
Weak

These evaluations can influence the direction and difficulty of subsequent questions.

The evaluation focuses on the candidate's technical understanding rather than only checking for exact keywords.

---

10. Final Feedback

Prompt / Development Goal

«Generate structured and actionable feedback after the interview is completed.»

AI Assistance

ChatGPT helped structure the final interview feedback into:

Summary
Strengths
Gaps
Next Steps

The feedback is intended to provide useful guidance rather than simply displaying a score.

The candidate should understand:

- What they performed well in
- Which technical areas need improvement
- What they should study or practice next

---

11. API Implementation

Prompt / Development Goal

«Implement the required HTTP endpoint according to the official Technical Specification.»

AI Assistance

ChatGPT helped implement the required interview endpoint:

POST /api/interview

The endpoint supports both starting an interview and continuing an existing interview session.

The implementation follows the supplied request and response structure rather than creating an unrelated API.

---

12. Frontend Development

Prompt / Development Goal

«Create a clean interface for selecting a candidate, conducting the interview, showing progress, and displaying the final report.»

AI Assistance

ChatGPT helped design the frontend experience with sections for:

- Candidate selection
- Candidate information
- Interview conversation
- Question progress
- Learning journey
- Answer input
- Interview completion
- Final feedback report

The interface was designed to make the interview feel like an actual technical interview rather than a simple form.

---

13. User Experience Improvements

Prompt / Development Goal

«Improve the interface so that the application feels polished and demonstrates the quality of the AI Interview Agent.»

AI Assistance

ChatGPT helped with:

- Layout organization
- Responsive design
- Interview progress indicators
- Candidate information display
- Feedback presentation
- Loading states
- Error handling
- Empty states
- Mobile-friendly styling

---

14. Testing Strategy

Prompt / Development Goal

«Test the interview agent with different types of candidate responses and identify potential edge cases.»

AI Assistance

ChatGPT suggested testing scenarios including:

Strong Answer

A technically detailed and correct response should lead to a deeper follow-up question.

Weak Answer

An incomplete or incorrect response should lead to clarification or a simpler conceptual question.

Short Answer

A very short response should not cause the interviewer to incorrectly assume strong understanding.

"I Don't Know"

The interviewer should handle uncertainty naturally and continue the interview appropriately.

Candidate With Limited Completed Topics

The system should avoid asking questions outside the candidate's completed learning journey when possible.

---

15. Debugging and Troubleshooting

ChatGPT was also used during development to help identify and resolve issues related to:

- Python environment setup
- Backend dependencies
- Frontend dependencies
- API communication
- JSON data handling
- Session state
- Frontend/backend integration
- Runtime errors
- Incorrect API responses
- UI behavior

AI suggestions were reviewed and adapted during implementation.

---

16. Documentation

Prompt / Development Goal

«Create clear documentation explaining how to install, run, test, and understand the project.»

AI Assistance

ChatGPT helped prepare:

- Project README
- Setup instructions
- Backend documentation
- Frontend documentation
- API explanation
- Environment variable instructions
- Testing guidance
- Hackathon submission preparation

---

17. Deployment Preparation

Prompt / Development Goal

«Prepare the project for deployment with a public GitHub repository and live demo.»

AI Assistance

ChatGPT helped identify the deployment requirements and prepare the project structure for:

- Public GitHub repository
- Backend deployment
- Frontend deployment
- Environment variables
- Production configuration
- Final API testing

Deployment configuration may be adjusted according to the hosting platform selected for the final submission.

---

18. AI-Assisted Development Philosophy

ChatGPT was used as a development assistant, not as a replacement for project decisions.

The development process involved:

Understand
    ↓
Plan
    ↓
Ask AI for implementation guidance
    ↓
Generate / modify code
    ↓
Run and test
    ↓
Identify issues
    ↓
Ask AI for debugging assistance
    ↓
Modify implementation
    ↓
Retest

The project was iteratively developed and reviewed during the hackathon.

---

19. Human Decisions

The following project decisions were made during development:

- Selecting Problem Statement 2
- Choosing the frontend and backend technology
- Deciding the overall user experience
- Deciding how candidate data should influence interviews
- Deciding how adaptive questioning should work
- Selecting the interview flow
- Reviewing AI-generated code
- Testing the application
- Deciding which improvements should be included
- Preparing the final submission

ChatGPT provided suggestions and implementation assistance, while project direction and final decisions were reviewed by the developer.

---

20. Final AI Usage Declaration

This project was developed using ChatGPT as the primary AI-assisted development tool.

ChatGPT was used for planning, architecture, coding assistance, debugging, testing guidance, UI improvements, API implementation guidance, documentation, and hackathon requirement analysis.

The supplied ABTalks curriculum, candidate profiles, and technical specification were used as the basis for the implementation.

The generated code and suggestions were reviewed, integrated, tested, and modified during the development process.

No claim is made that the project was created entirely without human involvement. The project represents an AI-assisted development workflow in which the developer directed the implementation, evaluated AI suggestions, tested the application, and made final decisions.

---

Development Summary

Problem Statement: The Interview Agent

AI Assistant: ChatGPT

Frontend: React + Vite

Backend: FastAPI + Python

AI: Gemini

Data: Official ABTalks curriculum and candidate profile resources

Core Features:

- Personalized technical interviews
- Multi-turn conversation
- Adaptive follow-up questions
- Curriculum-aware questioning
- Candidate learning journey analysis
- Session-based conversation context
- Minimum 8-question interview
- Multi-day curriculum coverage
- Structured final feedback
- Frontend interview experience
- API-based interview interaction

---

Final Checklist

Before submission, verify:

- [ ] GitHub repository is public
- [ ] Complete source code is available
- [ ] Official curriculum data is included
- [ ] Candidate data is included
- [ ] "PROMPTS.md" is included
- [ ] Backend API works
- [ ] Frontend works
- [ ] Interview reaches at least 8 questions
- [ ] At least 4 curriculum days are covered
- [ ] Follow-up questions adapt to answers
- [ ] Conversation context is maintained
- [ ] Final feedback is generated
- [ ] Live deployment is working
- [ ] Final API endpoint is tested
- [ ] Repository is tested from a clean setup
- [ ] Submission details are checked before the deadline

---

End of AI Usage Log


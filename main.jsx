import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { BrainCircuit, CheckCircle2, ChevronRight, Clock3, GraduationCap, RotateCcw, Send, Sparkles, Target, UserRound } from "lucide-react";
import "./styles.css";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const TOTAL_QUESTIONS = 8;

function App() {
  const [candidates, setCandidates] = useState([]);
  const [selected, setSelected] = useState(null);
  const [sessionId, setSessionId] = useState("");
  const [messages, setMessages] = useState([]);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [questionCount, setQuestionCount] = useState(0);
  const [coveredDays, setCoveredDays] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/candidates.json")
      .then(r => r.json())
      .then(data => setCandidates(data.candidates || []))
      .catch(() => setError("Could not load candidate profiles."));
  }, []);

  const passedMissions = useMemo(() => {
    if (!selected) return [];
    return selected.missions.filter(m => m.passed === true);
  }, [selected]);

  async function startInterview() {
    if (!selected) return;
    setLoading(true);
    setError("");
    setMessages([]);
    setFeedback(null);
    setDone(false);
    setAnswer("");
    const sid = crypto.randomUUID();
    setSessionId(sid);

    try {
      const res = await fetch(`${API_URL}/api/interview`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId: sid, candidate: selected })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Unable to start interview.");
      setMessages([{ role: "ai", text: data.reply }]);
      setQuestionCount(1);
      setCoveredDays([]);
    } catch (e) {
      setError(e.message);
      setSessionId("");
    } finally {
      setLoading(false);
    }
  }

  async function submitAnswer() {
    if (!answer.trim() || loading || done || !sessionId) return;
    const userText = answer.trim();
    setMessages(prev => [...prev, { role: "user", text: userText }]);
    setAnswer("");
    setLoading(true);
    setError("");

    try {
      const res = await fetch(`${API_URL}/api/interview`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId, message: userText })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Interview request failed.");

      if (data.done) {
        setMessages(prev => [...prev, { role: "ai", text: data.reply }]);
        setDone(true);
        setFeedback(data.feedback);
        setQuestionCount(TOTAL_QUESTIONS);
      } else {
        setMessages(prev => [...prev, { role: "ai", text: data.reply }]);
        setQuestionCount(prev => Math.min(TOTAL_QUESTIONS, prev + 1));
      }
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  function reset() {
    setSessionId("");
    setMessages([]);
    setFeedback(null);
    setDone(false);
    setAnswer("");
    setQuestionCount(0);
    setCoveredDays([]);
    setError("");
  }

  if (!selected) {
    return (
      <div className="app-shell">
        <header className="topbar">
          <div className="brand"><div className="brand-mark"><BrainCircuit size={22}/></div><div><strong>AI Interview Agent</strong><span>AI Cohort Technical Interviewer</span></div></div>
          <div className="status-pill"><span className="status-dot"/> AI READY</div>
        </header>
        <main className="landing">
          <section className="hero">
            <div className="eyebrow"><Sparkles size={15}/> PERSONALIZED TECHNICAL INTERVIEW</div>
            <h1>Test what you learned.<br/><span>Explain what you built.</span></h1>
            <p>Choose a cohort candidate and experience an adaptive technical interview based on their completed learning journey.</p>
          </section>
          <section className="candidate-grid">
            {candidates.map(c => (
              <button className="candidate-card" key={c.member.id} onClick={() => setSelected(c)}>
                <div className="avatar">{c.member.name.split(" ").map(x => x[0]).join("")}</div>
                <div className="candidate-main">
                  <div className="candidate-head"><h3>{c.member.name}</h3><span className="mini-status">COMPLETED</span></div>
                  <p>{c.member.jobRole}</p>
                  <div className="meta"><span>{c.member.yearsExperience} yrs</span><span>•</span><span>{c.member.education}</span></div>
                </div>
                <ChevronRight size={20} className="arrow"/>
              </button>
            ))}
          </section>
        </main>
      </div>
    );
  }

  if (!sessionId) {
    return (
      <div className="app-shell">
        <header className="topbar">
          <button className="brand brand-button" onClick={() => setSelected(null)}><div className="brand-mark"><BrainCircuit size={22}/></div><div><strong>AI Interview Agent</strong><span>AI Cohort Technical Interviewer</span></div></button>
          <button className="ghost-button" onClick={() => setSelected(null)}>Change candidate</button>
        </header>
        <main className="profile-layout">
          <section className="profile-card large-card">
            <div className="profile-hero">
              <div className="avatar big">{selected.member.name.split(" ").map(x => x[0]).join("")}</div>
              <div><div className="eyebrow">CANDIDATE PROFILE</div><h1>{selected.member.name}</h1><p>{selected.member.jobRole}</p></div>
            </div>
            <div className="stats-row">
              <div><span>Experience</span><strong>{selected.member.yearsExperience} years</strong></div>
              <div><span>Education</span><strong>{selected.member.education}</strong></div>
              <div><span>Missions passed</span><strong>{passedMissions.length}</strong></div>
            </div>
            <div className="section-title"><Target size={18}/> Completed learning journey</div>
            <div className="mission-list">
              {passedMissions.map(m => <div className="mission" key={m.day}><CheckCircle2 size={17}/><span>Day {m.day} · {m.title}</span><small>{m.attempts || 1} attempt{m.attempts === 1 ? "" : "s"}</small></div>)}
            </div>
            <button className="primary-button start-button" onClick={startInterview} disabled={loading || passedMissions.length < 4}>
              {loading ? "Starting..." : "Start Technical Interview"} <ChevronRight size={18}/>
            </button>
            {passedMissions.length < 4 && <p className="warning">This profile does not have enough passed curriculum days for the required interview.</p>}
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand"><div className="brand-mark"><BrainCircuit size={22}/></div><div><strong>AI Interview Agent</strong><span>Live technical interview</span></div></div>
        <div className="interview-header">
          <div className="progress-label"><span>INTERVIEW PROGRESS</span><strong>{Math.min(questionCount, TOTAL_QUESTIONS)} / {TOTAL_QUESTIONS}</strong></div>
          <div className="progress-track"><div style={{width: `${Math.min(100, (questionCount / TOTAL_QUESTIONS) * 100)}%`}}/></div>
          <button className="ghost-button" onClick={reset}><RotateCcw size={16}/> Exit</button>
        </div>
      </header>

      <main className="interview-layout">
        <aside className="sidebar">
          <div className="side-profile"><div className="avatar">{selected.member.name.split(" ").map(x => x[0]).join("")}</div><div><strong>{selected.member.name}</strong><span>{selected.member.jobRole}</span></div></div>
          <div className="side-section"><div className="side-title"><GraduationCap size={16}/> Learning journey</div>
            {passedMissions.slice(0, 10).map(m => <div className="side-mission" key={m.day}><span>Day {m.day}</span><span>{m.title}</span></div>)}
          </div>
          <div className="side-note"><Sparkles size={17}/><div><strong>Adaptive interviewer</strong><p>Questions use the candidate's completed topics and previous answers.</p></div></div>
        </aside>

        <section className="chat-panel">
          <div className="chat-title"><div><span className="eyebrow">TECHNICAL INTERVIEW</span><h2>Let's explore your engineering thinking.</h2></div><div className="live"><span/> LIVE</div></div>
          <div className="chat-scroll">
            {messages.map((m, i) => <div className={`message-row ${m.role}`} key={i}><div className="message-icon">{m.role === "ai" ? <BrainCircuit size={17}/> : <UserRound size={17}/>}</div><div className="bubble"><div className="message-label">{m.role === "ai" ? "AI INTERVIEWER" : "YOU"}</div><p>{m.text}</p></div></div>)}
            {loading && <div className="typing"><span/><span/><span/> AI is evaluating your answer…</div>}
            {error && <div className="error-box">{error}</div>}
          </div>
          {!done ? (
            <div className="composer">
              <textarea value={answer} onChange={e => setAnswer(e.target.value)} onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); submitAnswer(); } }} placeholder="Explain your answer in your own words..." disabled={loading}/>
              <div className="composer-footer"><span>Press Enter to submit · Shift + Enter for a new line</span><button className="send-button" onClick={submitAnswer} disabled={loading || !answer.trim()}><Send size={18}/></button></div>
            </div>
          ) : (
            <button className="primary-button report-button" onClick={() => document.getElementById("feedback")?.scrollIntoView({behavior:"smooth"})}>View Interview Report <ChevronRight size={18}/></button>
          )}
        </section>

        <aside className="metrics">
          <div className="metric-card"><div className="metric-icon"><Target size={18}/></div><span>Questions asked</span><strong>{questionCount}/{TOTAL_QUESTIONS}</strong></div>
          <div className="metric-card"><div className="metric-icon"><GraduationCap size={18}/></div><span>Curriculum days</span><strong>Adaptive</strong></div>
          <div className="metric-card"><div className="metric-icon"><Clock3 size={18}/></div><span>Mode</span><strong>Conversational</strong></div>
          {done && feedback && <div className="score-card"><span>OVERALL SCORE</span><strong>{feedback.score}</strong><small>/ 100</small><div className="score-bar"><div style={{width:`${feedback.score}%`}}/></div></div>}
        </aside>
      </main>

      {done && feedback && (
        <section id="feedback" className="feedback-section">
          <div className="feedback-heading"><div><div className="eyebrow">INTERVIEW REPORT</div><h2>Technical performance summary</h2></div><div className="report-score">{feedback.score}<span>/100</span></div></div>
          <div className="feedback-grid">
            <div className="feedback-card"><h3>Summary</h3><p>{feedback.summary}</p></div>
            <div className="feedback-card"><h3>Strengths</h3>{feedback.strengths.map((x,i)=><div className="feedback-item good" key={i}><CheckCircle2 size={17}/>{x}</div>)}</div>
            <div className="feedback-card"><h3>Gaps</h3>{feedback.gaps.map((x,i)=><div className="feedback-item gap" key={i}><span>!</span>{x}</div>)}</div>
            <div className="feedback-card"><h3>Next steps</h3>{feedback.next.map((x,i)=><div className="feedback-item next" key={i}><ChevronRight size={17}/>{x}</div>)}</div>
          </div>
          <button className="primary-button" onClick={reset}><RotateCcw size={18}/> Start another interview</button>
        </section>
      )}
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);

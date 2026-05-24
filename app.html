<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Campus Info Chatbot</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Syne:wght@700&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg: #f4f6fb;
    --sidebar-bg: #1a1f36;
    --sidebar-text: #c8cde8;
    --sidebar-accent: #4f8ef7;
    --card: #ffffff;
    --border: #e4e9f5;
    --text: #1a1f36;
    --muted: #7a82a6;
    --user-bubble: #1a1f36;
    --user-text: #ffffff;
    --bot-bubble: #ffffff;
    --bot-text: #1a1f36;
    --chip-bg: #eef2ff;
    --chip-text: #3a5bd9;
    --accent: #4f8ef7;
    --accent-dark: #2563eb;
    --green: #22c55e;
    --input-bg: #ffffff;
    --shadow: 0 2px 16px rgba(26,31,54,0.08);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    color: var(--text);
    height: 100vh;
    display: flex;
    overflow: hidden;
  }

  /* SIDEBAR */
  .sidebar {
    width: 260px; min-width: 260px;
    background: var(--sidebar-bg);
    display: flex; flex-direction: column;
    padding: 24px 16px 16px;
    gap: 20px;
    overflow-y: auto;
  }
  .sidebar-logo {
    display: flex; align-items: center; gap: 10px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
  .logo-icon {
    width: 38px; height: 38px; border-radius: 10px;
    background: var(--accent);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
  }
  .logo-text { font-family: 'Syne', sans-serif; font-size: 16px; color: #fff; }
  .logo-sub { font-size: 11px; color: var(--sidebar-text); margin-top: 1px; }

  .stat-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .stat-card {
    background: rgba(255,255,255,0.06);
    border-radius: 10px; padding: 10px 12px;
    text-align: center;
  }
  .stat-num { font-size: 22px; font-weight: 600; color: #fff; }
  .stat-lbl { font-size: 11px; color: var(--sidebar-text); margin-top: 2px; }

  .sb-section { font-size: 10px; font-weight: 600; color: rgba(200,205,232,0.5); letter-spacing: .1em; text-transform: uppercase; }

  .topic-grid { display: flex; flex-wrap: wrap; gap: 6px; }
  .topic-pill {
    font-size: 11px; padding: 4px 10px;
    background: rgba(79,142,247,0.15);
    color: #93bbfd;
    border-radius: 20px; cursor: pointer;
    border: 1px solid rgba(79,142,247,0.25);
    transition: background .2s;
  }
  .topic-pill:hover { background: rgba(79,142,247,0.3); }

  .hist-list { display: flex; flex-direction: column; gap: 4px; }
  .hist-item {
    font-size: 12px; color: var(--sidebar-text);
    padding: 6px 8px; border-radius: 8px;
    cursor: pointer; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis;
    transition: background .15s;
  }
  .hist-item:hover { background: rgba(255,255,255,0.08); color: #fff; }
  .hist-empty { font-size: 12px; color: rgba(200,205,232,0.35); }

  .sb-btn {
    width: 100%; padding: 8px 12px;
    border-radius: 9px; border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
    color: var(--sidebar-text);
    font-family: 'DM Sans', sans-serif;
    font-size: 12px; cursor: pointer;
    display: flex; align-items: center; gap: 8px;
    transition: background .15s;
  }
  .sb-btn:hover { background: rgba(255,255,255,0.1); color: #fff; }
  .sb-btns { display: flex; flex-direction: column; gap: 6px; margin-top: auto; }

  /* MAIN */
  .main {
    flex: 1; display: flex; flex-direction: column;
    overflow: hidden; background: var(--bg);
  }

  .topbar {
    background: var(--card);
    border-bottom: 1px solid var(--border);
    padding: 14px 24px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: var(--shadow);
  }
  .topbar-left { display: flex; align-items: center; gap: 10px; }
  .online-ring {
    width: 36px; height: 36px; border-radius: 50%;
    background: linear-gradient(135deg, #4f8ef7, #22c55e);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; color: #fff;
  }
  .topbar-title { font-family: 'Syne', sans-serif; font-size: 15px; color: var(--text); }
  .topbar-sub { font-size: 12px; color: var(--muted); display: flex; align-items: center; gap: 5px; }
  .online-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--green); }
  .topbar-time { font-size: 12px; color: var(--muted); }

  /* CHIPS */
  .chips-bar {
    background: var(--card);
    border-bottom: 1px solid var(--border);
    padding: 10px 20px;
    display: flex; gap: 8px; flex-wrap: wrap;
  }
  .chip {
    font-size: 12px; padding: 5px 12px;
    background: var(--chip-bg); color: var(--chip-text);
    border: 1px solid #d0dbff; border-radius: 20px;
    cursor: pointer; font-family: 'DM Sans', sans-serif;
    transition: all .15s;
  }
  .chip:hover { background: var(--accent); color: #fff; border-color: var(--accent); }

  /* MESSAGES */
  .messages {
    flex: 1; overflow-y: auto;
    padding: 24px 24px 16px;
    display: flex; flex-direction: column; gap: 14px;
    scroll-behavior: smooth;
  }
  .msg-row { display: flex; gap: 10px; align-items: flex-end; max-width: 75%; }
  .msg-row.user { align-self: flex-end; flex-direction: row-reverse; }
  .avatar {
    width: 32px; height: 32px; min-width: 32px;
    border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-size: 13px; font-weight: 600;
  }
  .avatar.bot { background: linear-gradient(135deg,#4f8ef7,#818cf8); color: #fff; }
  .avatar.usr { background: var(--user-bubble); color: #fff; }
  .msg-body { display: flex; flex-direction: column; gap: 4px; }
  .bubble {
    padding: 10px 14px; border-radius: 18px;
    font-size: 14px; line-height: 1.55;
    max-width: 100%;
  }
  .bubble.bot {
    background: var(--bot-bubble); color: var(--bot-text);
    border: 1px solid var(--border);
    border-bottom-left-radius: 4px;
    box-shadow: 0 1px 6px rgba(26,31,54,0.06);
  }
  .bubble.usr {
    background: var(--user-bubble); color: var(--user-text);
    border-bottom-right-radius: 4px;
  }
  .msg-meta { display: flex; align-items: center; gap: 8px; padding: 0 2px; }
  .msg-time { font-size: 11px; color: var(--muted); }
  .fb { background: none; border: none; cursor: pointer; font-size: 14px; opacity: .45; transition: opacity .15s, transform .15s; }
  .fb:hover { opacity: 1; transform: scale(1.2); }
  .fb.active { opacity: 1; }

  /* TYPING */
  .typing-row { display: flex; gap: 10px; align-items: flex-end; }
  .typing-bubble {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 18px; border-bottom-left-radius: 4px;
    padding: 12px 16px; display: flex; gap: 5px; align-items: center;
    box-shadow: 0 1px 6px rgba(26,31,54,0.06);
  }
  .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--muted); animation: bounce .9s infinite; }
  .dot:nth-child(2) { animation-delay: .15s; }
  .dot:nth-child(3) { animation-delay: .3s; }
  @keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-5px)} }

  /* INPUT */
  .input-area {
    background: var(--card);
    border-top: 1px solid var(--border);
    padding: 14px 20px;
    display: flex; gap: 10px; align-items: center;
  }
  .input-area input {
    flex: 1; padding: 11px 16px;
    border: 1.5px solid var(--border);
    border-radius: 24px;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px; color: var(--text);
    background: var(--input-bg);
    outline: none; transition: border .2s;
  }
  .input-area input:focus { border-color: var(--accent); }
  .send-btn {
    width: 42px; height: 42px; border-radius: 50%;
    background: var(--accent); border: none;
    color: #fff; font-size: 18px; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: background .15s, transform .1s;
    flex-shrink: 0;
  }
  .send-btn:hover { background: var(--accent-dark); }
  .send-btn:active { transform: scale(.95); }

  /* SCROLLBAR */
  .messages::-webkit-scrollbar { width: 4px; }
  .messages::-webkit-scrollbar-track { background: transparent; }
  .messages::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
  .sidebar::-webkit-scrollbar { width: 3px; }
  .sidebar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }

  /* TOAST */
  .toast {
    position: fixed; bottom: 30px; right: 30px;
    background: #1a1f36; color: #fff;
    padding: 10px 18px; border-radius: 10px;
    font-size: 13px; opacity: 0;
    transform: translateY(10px);
    transition: all .3s; pointer-events: none; z-index: 999;
  }
  .toast.show { opacity: 1; transform: translateY(0); }

  /* FADE IN */
  .msg-row { animation: fadeUp .25s ease; }
  @keyframes fadeUp { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
</style>
</head>
<body>

<!-- SIDEBAR -->
<div class="sidebar">
  <div class="sidebar-logo">
    <div class="logo-icon">🎓</div>
    <div>
      <div class="logo-text">CampusBot</div>
      <div class="logo-sub">Student Assistant</div>
    </div>
  </div>

  <div class="stat-row">
    <div class="stat-card">
      <div class="stat-num" id="q-count">0</div>
      <div class="stat-lbl">Questions</div>
    </div>
    <div class="stat-card">
      <div class="stat-num" id="helpful-count">0</div>
      <div class="stat-lbl">Helpful</div>
    </div>
  </div>

  <div class="sb-section">Topics</div>
  <div class="topic-grid">
    <span class="topic-pill" onclick="quickSend('Tell me about admissions')">Admissions</span>
    <span class="topic-pill" onclick="quickSend('Exam schedule')">Exams</span>
    <span class="topic-pill" onclick="quickSend('Hostel facilities')">Hostel</span>
    <span class="topic-pill" onclick="quickSend('Fee payment')">Fees</span>
    <span class="topic-pill" onclick="quickSend('Campus events')">Events</span>
    <span class="topic-pill" onclick="quickSend('Scholarship info')">Scholarships</span>
    <span class="topic-pill" onclick="quickSend('Placement cell')">Placements</span>
    <span class="topic-pill" onclick="quickSend('Club activities')">Clubs</span>
  </div>

  <div class="sb-section">Recent</div>
  <div class="hist-list" id="hist-list">
    <span class="hist-empty">No history yet</span>
  </div>

  <div class="sb-btns">
    <button class="sb-btn" onclick="clearChat()">🗑️ Clear chat</button>
    <button class="sb-btn" onclick="exportChat()">📥 Export JSON</button>
    <button class="sb-btn" onclick="exportTxt()">📄 Export as text</button>
  </div>
</div>

<!-- MAIN -->
<div class="main">
  <div class="topbar">
    <div class="topbar-left">
      <div class="online-ring">🤖</div>
      <div>
        <div class="topbar-title">Campus Info Chatbot</div>
        <div class="topbar-sub"><span class="online-dot"></span> Online &nbsp;·&nbsp; Ask anything about campus</div>
      </div>
    </div>
    <div class="topbar-time" id="topbar-time"></div>
  </div>

  <div class="chips-bar">
    <span class="chip" onclick="quickSend('Library hours')">📚 Library</span>
    <span class="chip" onclick="quickSend('Cafeteria menu')">🍽️ Cafeteria</span>
    <span class="chip" onclick="quickSend('Shuttle timings')">🚌 Shuttle</span>
    <span class="chip" onclick="quickSend('Academic calendar')">📅 Calendar</span>
    <span class="chip" onclick="quickSend('Health centre')">🏥 Health</span>
    <span class="chip" onclick="quickSend('Emergency contacts')">📞 Emergency</span>
    <span class="chip" onclick="quickSend('Wi-Fi on campus')">📶 Wi-Fi</span>
    <span class="chip" onclick="quickSend('Sports facilities')">🏅 Sports</span>
  </div>

  <div class="messages" id="msg-list"></div>

  <div class="input-area">
    <input type="text" id="chat-input" placeholder="Ask anything about campus…" onkeydown="if(event.key==='Enter')sendMsg()"/>
    <button class="send-btn" onclick="sendMsg()" title="Send">➤</button>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const REPLIES = {
  library: "📚 The Central Library is open Mon–Fri 8am–10pm, Sat 9am–6pm, Sun 10am–4pm. Digital resources are available 24/7 via the student portal at library.campus.edu.",
  cafeteria: "🍽️ Today's cafeteria menu: South Indian breakfast (7–10am), multi-cuisine lunch (12–2:30pm), evening snacks at the food court (3–6pm). Special diet options are available at Counter 3.",
  shuttle: "🚌 Campus shuttles run every 20 mins from 7am–9pm. Route A: Main Gate → Hostel Block. Route B: Main Gate → Academic Block. Download the CampusGo app for live tracking.",
  calendar: "📅 Key dates — Semester exams: June 10 | Mid-term break: June 2–5 | Annual Fest: July 14–18 | Results: July 30. Full calendar available on the student portal under 'Academics'.",
  health: "🏥 Health Centre is in Block C, Ground Floor. Open Mon–Sat 8am–8pm. On-call doctor available 24/7 for emergencies. Call ext. 1122 or walk in. Free consultation for students.",
  emergency: "🚨 Campus Security: +91-40-1234-5678 | Health Centre: ext. 1122 | Admin Office: ext. 1000 | Fire: 101 | Ambulance: 108. All lines are active 24/7.",
  admission: "🎓 Admissions for 2025–26 are open! Apply online at admissions.campus.edu. Entrance exams in April. Merit scholarships available for top scorers. Deadline: March 31.",
  hostel: "🏠 Hostel registration opens in July. Separate blocks for boys and girls. Fees: ₹8,500/month (AC) | ₹5,500/month (non-AC), meals included. Apply on the portal under 'Hostel'.",
  fee: "💳 Pay fees online via the student portal — UPI, net banking, and cards accepted. Current semester deadline: May 31. Late fee ₹500/week applies after deadline. Receipts auto-emailed.",
  exam: "📝 Exam schedules are published on the portal 2 weeks before exams. Hall tickets available 3 days prior. Carry your ID card. Results declared within 3 weeks of last exam.",
  event: "🎉 Upcoming events — Tech Fest: July 14–16 | Cultural Night: July 17 | Sports Meet: Aug 3–5 | Hackathon: Aug 20. Register on the portal under 'Student Activities'.",
  wifi: "📶 Campus Wi-Fi network: 'CampusNet'. Login with your student ID and portal password. Available in all academic blocks, library, and hostels. Speed: 100 Mbps. IT helpdesk: ext. 2200.",
  sports: "🏅 Sports facilities include a cricket ground, football field, basketball & volleyball courts, indoor badminton hall, swimming pool (9am–6pm), and a fully-equipped gym.",
  scholarship: "🏆 Scholarships available: Merit (top 10% students), Sports, Cultural, and Need-based. Apply on the portal under 'Scholarships' by April 15. Documents: marksheets + income certificate.",
  placement: "💼 Placement Cell is in Block D, Room 401. 200+ companies visited last year. Average package: ₹6.8 LPA. Register at placements.campus.edu. Pre-placement training every Saturday.",
  club: "🎨 Active clubs: Coding Club, Photography, Drama, Music Band, Robotics, Literary Society, NSS, NCC. Join via the Student Activities portal or visit the Student Union office.",
};

function matchReply(txt) {
  const t = txt.toLowerCase();
  if (t.includes('library') || t.includes('book')) return REPLIES.library;
  if (t.includes('cafeteria') || t.includes('menu') || t.includes('food') || t.includes('canteen')) return REPLIES.cafeteria;
  if (t.includes('shuttle') || t.includes('bus') || t.includes('transport')) return REPLIES.shuttle;
  if (t.includes('calendar') || t.includes('academic') || t.includes('schedule') && !t.includes('exam')) return REPLIES.calendar;
  if (t.includes('health') || t.includes('doctor') || t.includes('medical') || t.includes('clinic')) return REPLIES.health;
  if (t.includes('emergency') || t.includes('contact')) return REPLIES.emergency;
  if (t.includes('admission') || t.includes('apply') || t.includes('application')) return REPLIES.admission;
  if (t.includes('hostel') || t.includes('dormitory') || t.includes('accommodation')) return REPLIES.hostel;
  if (t.includes('fee') || t.includes('payment') || t.includes('tuition')) return REPLIES.fee;
  if (t.includes('exam') || t.includes('hall ticket') || t.includes('result')) return REPLIES.exam;
  if (t.includes('event') || t.includes('fest') || t.includes('festival')) return REPLIES.event;
  if (t.includes('wi-fi') || t.includes('wifi') || t.includes('internet') || t.includes('network')) return REPLIES.wifi;
  if (t.includes('sport') || t.includes('gym') || t.includes('pool') || t.includes('cricket') || t.includes('football')) return REPLIES.sports;
  if (t.includes('scholarship') || t.includes('merit') || t.includes('award')) return REPLIES.scholarship;
  if (t.includes('placement') || t.includes('job') || t.includes('career') || t.includes('company') || t.includes('recruit')) return REPLIES.placement;
  if (t.includes('club') || t.includes('activit') || t.includes('society') || t.includes('nss') || t.includes('ncc')) return REPLIES.club;
  return "🤔 That's a great question! For details not covered here, visit the Student Services desk (Admin Block, Room 101), email info@campus.edu, or call the helpline at +91-40-1234-0000.";
}

let qCount = 0, helpfulCount = 0, history = [], messages = [];

function getTime() {
  return new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
}

function updateClock() {
  document.getElementById('topbar-time').textContent = new Date().toLocaleString([], {
    weekday:'short', month:'short', day:'numeric', hour:'2-digit', minute:'2-digit'
  });
}
updateClock(); setInterval(updateClock, 30000);

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2500);
}

function addMessage(role, text) {
  const list = document.getElementById('msg-list');
  const ts = getTime();
  messages.push({role, text, time: ts});

  const row = document.createElement('div');
  row.className = 'msg-row ' + (role === 'user' ? 'user' : '');

  const av = document.createElement('div');
  av.className = 'avatar ' + (role === 'user' ? 'usr' : 'bot');
  av.textContent = role === 'user' ? 'ME' : '🤖';

  const body = document.createElement('div');
  body.className = 'msg-body';

  const bub = document.createElement('div');
  bub.className = 'bubble ' + (role === 'user' ? 'usr' : 'bot');
  bub.textContent = text;

  const meta = document.createElement('div');
  meta.className = 'msg-meta';
  const timeEl = document.createElement('span');
  timeEl.className = 'msg-time'; timeEl.textContent = ts;
  meta.appendChild(timeEl);

  if (role === 'assistant') {
    const up = document.createElement('button');
    up.className = 'fb'; up.textContent = '👍'; up.title = 'Helpful';
    const dn = document.createElement('button');
    dn.className = 'fb'; dn.textContent = '👎'; dn.title = 'Not helpful';
    up.onclick = () => {
      if (!up.classList.contains('active')) {
        up.classList.add('active'); dn.classList.remove('active');
        helpfulCount++; document.getElementById('helpful-count').textContent = helpfulCount;
        showToast('Thanks for the feedback! 👍');
      }
    };
    dn.onclick = () => {
      dn.classList.add('active'); up.classList.remove('active');
      showToast("We'll work on improving that.");
    };
    meta.appendChild(up); meta.appendChild(dn);
  }

  body.appendChild(bub); body.appendChild(meta);
  row.appendChild(av); row.appendChild(body);
  list.appendChild(row);
  list.scrollTop = list.scrollHeight;
}

function showTyping() {
  const list = document.getElementById('msg-list');
  const row = document.createElement('div');
  row.className = 'typing-row'; row.id = 'typing';
  const av = document.createElement('div');
  av.className = 'avatar bot'; av.textContent = '🤖';
  const bub = document.createElement('div');
  bub.className = 'typing-bubble';
  bub.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
  row.appendChild(av); row.appendChild(bub);
  list.appendChild(row); list.scrollTop = list.scrollHeight;
}
function hideTyping() { const r = document.getElementById('typing'); if (r) r.remove(); }

function updateHistory(text) {
  history.unshift(text.slice(0, 38) + (text.length > 38 ? '…' : ''));
  history = history.slice(0, 6);
  const hl = document.getElementById('hist-list');
  hl.innerHTML = history.map(h =>
    `<div class="hist-item" onclick="quickSend('${h.replace(/'/g,"\\'")}')">💬 ${h}</div>`
  ).join('');
}

function quickSend(txt) {
  document.getElementById('chat-input').value = txt;
  sendMsg();
}

function sendMsg() {
  const inp = document.getElementById('chat-input');
  const txt = inp.value.trim(); if (!txt) return;
  inp.value = '';
  addMessage('user', txt);
  qCount++; document.getElementById('q-count').textContent = qCount;
  updateHistory(txt);
  showTyping();
  const delay = 800 + Math.random() * 700;
  setTimeout(() => { hideTyping(); addMessage('assistant', matchReply(txt)); }, delay);
}

function clearChat() {
  document.getElementById('msg-list').innerHTML = '';
  messages = []; history = []; qCount = 0; helpfulCount = 0;
  document.getElementById('q-count').textContent = '0';
  document.getElementById('helpful-count').textContent = '0';
  document.getElementById('hist-list').innerHTML = '<span class="hist-empty">No history yet</span>';
  addMessage('assistant', '👋 Chat cleared! How can I help you today?');
}

function exportChat() {
  const blob = new Blob([JSON.stringify(messages, null, 2)], {type: 'application/json'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
  a.download = 'campus_chat_' + Date.now() + '.json'; a.click();
  showToast('Chat exported as JSON!');
}

function exportTxt() {
  const txt = messages.map(m => `[${m.time}] ${m.role === 'user' ? 'You' : 'Bot'}: ${m.text}`).join('\n');
  const blob = new Blob([txt], {type: 'text/plain'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
  a.download = 'campus_chat_' + Date.now() + '.txt'; a.click();
  showToast('Chat exported as text!');
}

// Welcome message
addMessage('assistant', "👋 Hi! I'm your Campus Info Assistant. Ask me anything about library, cafeteria, exams, hostel, fees, events, and more! Or tap a quick chip above to get started.");
</script>
</body>
</html>

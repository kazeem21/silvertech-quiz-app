import streamlit as st
import json
import random
import time
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

# --- Configuration ---
QUESTIONS_FILE = Path("questions.json")
STATE_FILE = Path("game_state.json")
TEACHER_PASSWORD = "letmein"  # change this before real use

# --- Utility functions ---
def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def init_state(num_questions):
    if not STATE_FILE.exists():
        state = {
            "current_q_index": -1,
            "players": {},
            "question_order": random.sample(list(range(num_questions)), num_questions),
            "started": False,
            "finished": False,
            "last_update": time.time(),
            "reveal_explanation": False
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f)
    return load_state()

def load_state():
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    state['last_update'] = time.time()
    with open(STATE_FILE, "w", encoding='utf-8') as f:
        json.dump(state, f)

def reset_state(num_questions):
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    return init_state(num_questions)

# --- Quiz helpers ---
def get_current_question(state, questions):
    idx = state["current_q_index"]
    if idx == -1:
        return None
    real_idx = state["question_order"][idx]
    q = questions[real_idx]
    return {
        "q_index": idx,
        "question_id": real_idx,
        "text": q["question"],
        "options": q["options"],
        "answer": q["answer"],
        "explanation": q.get("explanation", "No explanation provided.")
    }

def add_player(state, name):
    if name not in state["players"]:
        state["players"][name] = {"score": 0, "answered_qs": []}

def submit_answer(state, player_name, q_index, chosen):
    if player_name not in state["players"]:
        return False, "Player not registered."
    player = state["players"][player_name]
    if q_index in player["answered_qs"]:
        return False, "Already answered this question."

    questions = load_questions()
    real_qid = state["question_order"][q_index]
    q = questions[real_qid]
    correct = q["answer"]

    if chosen == correct:
        player["score"] += 1
        result = True
    else:
        result = False

    player["answered_qs"].append(q_index)
    state["players"][player_name] = player
    save_state(state)
    return result, correct

# --- Feedback Animation ---
def show_feedback(is_correct, explanation=None):
    """
    Display animated feedback for student's answer.
    """
    if is_correct:
        st.markdown(
            """
            <div style="
                color: #00ff00;
                font-size: 28px;
                font-weight: bold;
                text-align: center;
                animation: glow 1s ease-in-out infinite alternate;
            ">
                ✅ Correct!
            </div>
            <style>
                @keyframes glow {
                    from { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00, 0 0 30px #00ff00; }
                    to   { text-shadow: 0 0 20px #33ff33, 0 0 30px #33ff33, 0 0 40px #33ff33; }
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        if explanation:
            st.info(f"📘 Explanation: {explanation}")
    else:
        st.markdown(
            """
            <div style="
                color: #ff3333;
                font-size: 28px;
                font-weight: bold;
                text-align: center;
                animation: pulse 1s infinite;
            ">
                ❌ Wrong!
            </div>
            <style>
                @keyframes pulse {
                    0% { text-shadow: 0 0 5px #ff0000; }
                    50% { text-shadow: 0 0 25px #ff4444; }
                    100% { text-shadow: 0 0 5px #ff0000; }
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        if explanation:
            st.info(f"📘 Explanation: {explanation}")

# --- Streamlit Layout ---
st.set_page_config(page_title="SILVERTECH Edu-consult", layout="wide")
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0b0b0b, #1a1a1a, #10111f);
        font-family: 'Segoe UI', sans-serif;
        color: #f2f2f2;
    }

    /* Headings */
    h1, h2, h3, h4 {
        font-family: 'Segoe UI Semibold', sans-serif;
        color: #00e0ff;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111, #222);
        color: #f2f2f2;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
        color: #ff66cc;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border-radius: 14px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        transition: all 0.25s ease-in-out;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #0072ff, #00c6ff);
        transform: scale(1.07);
    }

    /* Radio options */
    div[data-baseweb="radio"] {
        padding: 12px 16px;
        background: #1e1e2e;
        border: 1px solid #333;
        border-radius: 12px;
    }
    div[data-baseweb="radio"] label {
        color: #e0e0e0 !important;
        font-size: 1.05em;
    }

    /* Alerts */
    .stAlert {
        border-radius: 14px !important;
        font-size: 0.95em;
        font-weight: 500;
    }

    /* Leaderboard styling */
    .leaderboard-entry {
        font-size: 1.1em;
        padding: 8px;
        margin: 6px 0;
        border-bottom: 1px solid #444;
        color: #f2f2f2;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#004080;'>TANZEEL COLLEGES INTERNATIONAL, MARARABA</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#008080;'>📚 1st Term(2025/26) Inter-Class Live Quiz Competition</h3>", unsafe_allow_html=True)
st.markdown("---")

# Load questions
try:
    questions = load_questions()
except Exception as e:
    st.error(f"Could not load questions.json: {e}")
    st.stop()

state = init_state(len(questions))

# --- Mode Selector ---
mode = st.sidebar.selectbox("🔑 Choose mode", ["Student", "Teacher / Admin"], key="mode_selector")

# ------------------ TEACHER VIEW ------------------ #
if mode == "Teacher / Admin":
    pw = st.sidebar.text_input("Teacher password", type="password", key="teacher_pw")
    if pw != TEACHER_PASSWORD:
        st.warning("Enter teacher password to see admin controls.")
    else:
        st.subheader("🎓 Quiz Master Controls")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("▶️ Start / Restart Quiz", key="start_btn"):
                state = reset_state(len(questions))
                state["started"] = True
                state["current_q_index"] = 0
                save_state(state)
                st.success("✅ Quiz restarted and started. First question active.")

        with col2:
            if st.button("⏭ Next Question", key="next_btn"):
                if not state["started"]:
                    st.warning("⚠️ Quiz not started yet.")
                else:
                    if state["current_q_index"] < len(state["question_order"]) - 1:
                        state["current_q_index"] += 1
                        state["reveal_explanation"] = False
                        save_state(state)
                        st.info(f"➡️ Moved to question #{state['current_q_index']+1}")
                    else:
                        state["finished"] = True
                        save_state(state)
                        st.success("🏁 Quiz finished.")

        with col3:
            if st.button("⏹ End Quiz", key="end_btn"):
                state["finished"] = True
                save_state(state)
                st.success("🚫 Quiz marked finished.")

        with col4:
            if st.button("💡 Reveal Explanation", key="reveal_btn"):
                state["reveal_explanation"] = True
                save_state(state)

        st.subheader("🏆 Live Leaderboard")
        state = load_state()
        players = state.get("players", {})
        if players:
            leaderboard = sorted(players.items(), key=lambda kv: kv[1]['score'], reverse=True)
            for i, (name, data) in enumerate(leaderboard, start=1):
                st.write(f"**{i}. {name} — {data['score']} pts**")
        else:
            st.write("No players yet.")

        st.subheader("👀 Question Preview")
        q = get_current_question(state, questions)
        if q:
            st.markdown(f"**Q{state['current_q_index']+1}: {q['text']}**")
            for opt in q['options']:
                st.write(opt)
            if state.get("reveal_explanation", False):
                st.success(f"✅ Correct Answer: {q['answer']}")
                st.info(f"📘 Explanation: {q['explanation']}")
        else:
            st.write("No question active. Start the quiz to begin.")

# ------------------ STUDENT VIEW ------------------ #
else:
    st.subheader("🙋 Student / Participant View")
    st_autorefresh(interval=3000, key="student_refresh")

    name = st.text_input("✍️ Enter your name (as in register)", key="student_name")
    if not name:
        st.info("Please enter your name to join.")
        st.stop()

    state = load_state()
    add_player(state, name)
    save_state(state)

    st.write(f"👋 Hello **{name}**, wait for teacher to start the quiz.")

    if state.get("finished", False):
        st.success("🏁 This quiz has finished. See leaderboard below.")

    q = get_current_question(state, questions)

    if not state.get("started", False) or q is None:
        st.info("⏳ No active question. Wait for the teacher to start.")
    else:
        st.markdown(f"### ❓ Question #{state['current_q_index']+1}")
        st.markdown(f"**{q['text']}**")

        if "last_q_index" not in st.session_state or st.session_state.last_q_index != q["q_index"]:
            st.session_state.submitted = False
            st.session_state.last_q_index = q["q_index"]

        choice = st.radio("👉 Choose an option:", q["options"], key=f"choice_{name}_{q['q_index']}")

        if not st.session_state.get("submitted", False):
            if st.button("✅ Submit Answer", key=f"submit_{q['q_index']}_{name}"):
                state = load_state()
                res, correct = submit_answer(state, name, q["q_index"], choice)

                questions = load_questions()
                real_qid = state["question_order"][q["q_index"]]
                q_full = questions[real_qid]
                explanation = q_full.get("explanation", "No explanation provided.")

                show_feedback(res, explanation if res else f"Correct answer: {correct}\n{explanation}")

                st.session_state.submitted = True
        else:
            st.warning("⏳ Answer already submitted. Waiting for teacher to move on...")

        st.markdown("#### 📊 Your Current Score")
        player = state["players"].get(name, {"score": 0})
        st.write(f"**{player['score']} points**")

        st.markdown("#### 🏆 Live Leaderboard (Top 10)")
        players = state.get("players", {})
        if players:
            leaderboard = sorted(players.items(), key=lambda kv: kv[1]['score'], reverse=True)[:10]
            for i, (pname, pdata) in enumerate(leaderboard, start=1):
                st.write(f"**{i}. {pname} — {pdata['score']} pts**")
        else:
            st.write("No players yet.")

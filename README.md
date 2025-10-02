
Streamlit In-Class Quiz Prototype
=================================

Files created:
- quiz_app.py        : The Streamlit app (single-file)
- questions.json     : Sample multiple-choice questions
- game_state.json    : created at runtime when you start the app

How to run (on your laptop in the classroom):
1. Install requirements (recommended in a virtual environment):
   pip install streamlit

2. Copy the folder `streamlit_quiz` to a folder on your laptop, or run directly:
   streamlit run quiz_app.py --server.address 0.0.0.0 --server.port 8501

3. Find your laptop's local IP address (e.g., 192.168.0.101).
   Students connect using: http://<your-ip>:8501
   Example: http://192.168.0.101:8501

4. Teacher mode:
   - Open the app, choose "Teacher / Admin" on the sidebar.
   - Enter the teacher password (default: letmein). Change this in quiz_app.py.
   - Use "Start / Restart Quiz" and "Next Question" to control the flow.

5. Student mode:
   - Students open the URL on their devices, choose "Student" mode, enter name and wait.
   - When teacher advances the question, students answer and submit.
   - Leaderboard updates live in both Teacher and Student views.

Notes & Caveats:
- This is a prototype using a simple file (game_state.json) to coordinate state between users.
  For small in-class use (10-50 students) on the same WiFi this works well.
- If you expect many simultaneous users or want robustness, consider migrating the state
  to a lightweight database (SQLite) or using a dedicated real-time backend (Flask-SocketIO).
- Change TEACHER_PASSWORD in quiz_app.py before using in real assessment situations.
- Ensure your laptop firewall allows incoming connections on the chosen port (8501).

import streamlit as st
import json
import datetime
import os

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="centered"
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

mode = st.session_state.dark_mode

if mode:
    bg = "#0f1117"
    card = "#1e293b"
    card2 = "#0f172a"
    text = "#f1f5f9"
    sub = "#94a3b8"
    border = "#334155"
    input_bg = "#1e293b"
else:
    bg = "#f5f5f7"
    card = "#ffffff"
    card2 = "#f0f0f5"
    text = "#1d1d1f"
    sub = "#6e6e73"
    border = "#d2d2d7"
    input_bg = "#ffffff"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }}
.stApp {{ background: {bg} !important; }}
h1, h2, h3, h4, h5, p, div, span, label {{ color: {text} !important; }}
.apple-card {{
    background: {card};
    border-radius: 20px;
    padding: 20px 24px;
    margin: 10px 0;
    box-shadow: 0 2px 20px rgba(0,0,0,{'0.3' if mode else '0.08'});
    border: 1px solid {border};
}}
.task-row {{
    background: {card};
    border-radius: 16px;
    padding: 14px 18px;
    margin: 6px 0;
    box-shadow: 0 1px 10px rgba(0,0,0,{'0.2' if mode else '0.06'});
    border: 1px solid {border};
}}
.subject-badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3px;
}}
.timer-display {{
    font-size: 52px;
    font-weight: 300;
    letter-spacing: -2px;
    text-align: center;
    color: {text} !important;
    padding: 10px 0;
}}
.perfect-week {{
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: white !important;
    padding: 18px;
    border-radius: 20px;
    text-align: center;
    font-size: 20px;
    font-weight: 700;
    margin: 12px 0;
    box-shadow: 0 4px 20px rgba(245,158,11,0.4);
}}
.stButton > button {{
    border-radius: 12px !important;
    border: 1px solid {border} !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(0,0,0,{'0.3' if mode else '0.1'}) !important;
    background: {card} !important;
    color: {text} !important;
}}
.stButton > button p {{ color: {text} !important; }}
.stButton > button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,{'0.4' if mode else '0.15'}) !important;
}}
.stTextInput > div > div > input,
.stNumberInput > div > div > input {{
    border-radius: 12px !important;
    border: 1px solid {border} !important;
    background: {input_bg} !important;
    color: {text} !important;
}}
.stProgress > div > div > div {{ border-radius: 100px !important; }}
div[data-testid="stMetricValue"] {{ font-size: 24px !important; font-weight: 600 !important; color: {text} !important; }}
div[data-testid="stMetricLabel"] {{ font-size: 12px !important; color: {sub} !important; }}
.stTabs [data-baseweb="tab-list"] {{
    background: {card2} !important;
    border-radius: 14px !important;
    padding: 4px !important;
    gap: 4px !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 10px !important;
    color: {sub} !important;
    font-weight: 500 !important;
    font-size: 13px !important;
}}
.stTabs [aria-selected="true"] {{
    background: {card} !important;
    color: {text} !important;
    box-shadow: 0 1px 8px rgba(0,0,0,0.15) !important;
}}
</style>
""", unsafe_allow_html=True)

COLORS = {
    "수학": "#FF6B6B",
    "영어": "#4ECDC4",
    "국어": "#F59E0B",
    "과학": "#6BCB77",
    "사회": "#A78BFA",
    "역사": "#F9A03F",
    "기타": "#94A3B8",
}

DATA_FILE = "planner_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tasks": [], "weekly_record": {}, "study_time_record": {}}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "tasks": st.session_state.tasks,
            "weekly_record": st.session_state.weekly_record,
            "study_time_record": st.session_state.get("study_time_record", {})
        }, f, ensure_ascii=False, indent=2)

if "tasks" not in st.session_state:
    data = load_data()
    st.session_state.tasks = data["tasks"]
    st.session_state.weekly_record = data["weekly_record"]
    st.session_state.study_time_record = data.get("study_time_record", {})

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None
if "timer_elapsed" not in st.session_state:
    st.session_state.timer_elapsed = 0
if "timer_subject" not in st.session_state:
    st.session_state.timer_subject = "수학"

KST = datetime.timezone(datetime.timedelta(hours=9))
now_kst = datetime.datetime.now(KST)
today = now_kst.strftime("%Y-%m-%d")
today_tasks = [t for t in st.session_state.tasks if t["date"] == today]
done_count = sum(1 for t in today_tasks if t["done"])
total_count = len(today_tasks)

col_title, col_toggle = st.columns([0.8, 0.2])
with col_title:
    st.markdown("# 📚 AI Study Planner")
with col_toggle:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🌙" if mode else "☀️", key="toggle_mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["⏱ 타이머", "📋 할 일", "📊 주간 통계", "🤖 AI 조언"])

with tab1:
    subject_time = {}
    for task in st.session_state.tasks:
        if task["done"]:
            s = task["subject"]
            subject_time[s] = subject_time.get(s, 0) + task["duration"]

    if subject_time:
        st.markdown("### 과목별 공부 비율")
        total = sum(subject_time.values())
        for subj, mins in sorted(subject_time.items(), key=lambda x: -x[1]):
            color = COLORS.get(subj, "#94A3B8")
            pct = round(mins / total * 100)
            st.markdown(f"""
            <div style="margin: 6px 0;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="font-size:13px; font-weight:600; color:{text};">
                        <span style="display:inline-block; width:10px; height:10px;
                               border-radius:50%; background:{color}; margin-right:6px;"></span>
                        {subj}
                    </span>
                    <span style="font-size:13px; color:{sub};">{mins}분 ({pct}%)</span>
                </div>
                <div style="background:{border}; border-radius:100px; height:8px;">
                    <div style="background:{color}; width:{pct}%; height:8px; border-radius:100px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="apple-card" style="text-align:center; padding:30px;">
            <div style="font-size:36px">📊</div>
            <div style="font-size:14px; color:{sub}; margin-top:8px">할 일을 완료하면 과목별 비율이 나와요!</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    timer_subject = st.selectbox("공부할 과목", list(COLORS.keys()), key="timer_subject_select")

    if st.session_state.timer_running and st.session_state.timer_start:
        elapsed = st.session_state.timer_elapsed + (datetime.datetime.now() - st.session_state.timer_start).seconds
        start_time = st.session_state.timer_start.strftime("%H:%M")
        st.markdown(f"""
        <div class="apple-card" style="text-align:center; padding:24px;">
            <div style="font-size:28px;">⏱</div>
            <div style="font-size:18px; font-weight:600; margin-top:8px; color:{text};">
                {st.session_state.timer_subject} 공부 중...
            </div>
            <div style="font-size:13px; color:{sub}; margin-top:6px;">
                시작 시간: {start_time}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        elapsed = st.session_state.timer_elapsed
        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60
        st.markdown(f'<div class="timer-display">{h:02d}:{m:02d}:{s:02d}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if not st.session_state.timer_running:
            if st.button("▶ 시작", use_container_width=True, key="btn_start"):
                st.session_state.timer_running = True
                st.session_state.timer_start = datetime.datetime.now(KST)
                st.session_state.timer_subject = timer_subject
                st.rerun()
        else:
            if st.button("⏸ 일시정지", use_container_width=True, key="btn_pause"):
                elapsed_now = (datetime.datetime.now() - st.session_state.timer_start).seconds
                st.session_state.timer_elapsed += elapsed_now
                st.session_state.timer_running = False
                st.session_state.timer_start = None
                st.rerun()
    with col2:
        if st.button("⏹ 종료", use_container_width=True, key="btn_stop"):
            if st.session_state.timer_running and st.session_state.timer_start:
                elapsed_now = (datetime.datetime.now() - st.session_state.timer_start).seconds
                st.session_state.timer_elapsed += elapsed_now
            total_mins = round(st.session_state.timer_elapsed / 60)
            if total_mins > 0:
                study_record = st.session_state.get("study_time_record", {})
                study_record[today] = study_record.get(today, 0) + total_mins
                st.session_state.study_time_record = study_record
                save_data()
                st.success(f"🎉 {st.session_state.timer_subject} {total_mins}분 공부 완료!")
            st.session_state.timer_running = False
            st.session_state.timer_start = None
            st.session_state.timer_elapsed = 0
            st.rerun()
    with col3:
        if st.button("🔄 리셋", use_container_width=True, key="btn_reset"):
            st.session_state.timer_running = False
            st.session_state.timer_start = None
            st.session_state.timer_elapsed = 0
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"**오늘 진행률: {done_count}/{total_count} 완료**")
    st.progress(done_count / total_count if total_count > 0 else 0)

with tab2:
    st.markdown("### 📋 오늘의 할 일")

    if not today_tasks:
        st.markdown(f"""
        <div class="apple-card" style="text-align:center; padding:30px;">
            <div style="font-size:36px">📝</div>
            <div style="font-size:14px; color:{sub}; margin-top:8px">오늘 할 일이 없어요. 아래에서 추가해봐요!</div>
        </div>
        """, unsafe_allow_html=True)

    for i, task in enumerate(st.session_state.tasks):
        if task["date"] != today:
            continue
        color = COLORS.get(task["subject"], "#94A3B8")
        col1, col2, col3 = st.columns([0.08, 0.72, 0.2])
        with col1:
            checked = st.checkbox("", value=task["done"], key=f"chk_{i}")
            if checked != task["done"]:
                st.session_state.tasks[i]["done"] = checked
                if all(t["done"] for t in today_tasks):
                    st.session_state.weekly_record[today] = True
                save_data()
                st.rerun()
        with col2:
            done_style = "opacity:0.4; text-decoration:line-through;" if task["done"] else ""
            st.markdown(f"""
            <div class="task-row" style="{done_style}">
                <span class="subject-badge" style="background:{color}22; color:{color};">{task['subject']}</span>
                <strong style="margin-left:8px; font-size:14px;">{task['title']}</strong>
                <span style="color:{sub}; font-size:12px; margin-left:8px;">⏱ {task['duration']}분</span>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            if st.button("🗑", key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                save_data()
                st.rerun()

    st.markdown("---")
    st.markdown("### ➕ 할 일 추가")
    subject = st.selectbox("과목", list(COLORS.keys()), key="add_subject")
    title = st.text_input("할 일 내용", key="add_title")
    duration = st.number_input("예상 시간 (분)", min_value=5, max_value=300, step=5, value=30, key="add_duration")

    if st.button("✅ 추가하기", use_container_width=True, key="btn_add"):
        if title.strip():
            st.session_state.tasks.append({
                "subject": subject,
                "title": title,
                "duration": int(duration),
                "done": False,
                "date": today
            })
            save_data()
            st.success(f"추가됨: [{subject}] {title}")
            st.rerun()
        else:
            st.warning("할 일을 입력해주세요!")

with tab3:
    st.markdown("### 📊 주간 통계")

    today_date = datetime.date.today()
    monday = today_date - datetime.timedelta(days=today_date.weekday())
    week_days = [(monday + datetime.timedelta(days=i)).isoformat() for i in range(7)]
    day_names = ["월", "화", "수", "목", "금", "토", "일"]
    completed_days = sum(1 for d in week_days if st.session_state.weekly_record.get(d))

    st.markdown("#### 이번 주 일과 현황")
    cols = st.columns(7)
    for i, (col, d, name) in enumerate(zip(cols, week_days, day_names)):
        with col:
            day_tasks = [t for t in st.session_state.tasks if t["date"] == d]
            if not day_tasks:
                color = border
            elif st.session_state.weekly_record.get(d):
                color = "#22c55e"
            else:
                color = "#ef4444"
            done = sum(1 for t in day_tasks if t["done"])
            total = len(day_tasks)
            st.markdown(f"""
            <div style="text-align:center">
                <div style="font-size:11px; color:{sub}; margin-bottom:6px; font-weight:500;">{name}</div>
                <div style="background:{color}; height:80px; border-radius:12px;
                            display:flex; align-items:flex-end; justify-content:center;
                            padding-bottom:8px; font-size:11px; color:white; font-weight:600;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
                    {done}/{total}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"**이번 주 완료한 날: {completed_days} / 7일**")
    st.progress(completed_days / 7)

    if completed_days == 7:
        st.markdown('<div class="perfect-week">🏆 PERFECT WEEK! 대단해요!</div>', unsafe_allow_html=True)
    elif completed_days >= 5:
        st.success("🔥 거의 다 왔어요! 조금만 더!")
    else:
        st.info(f"💪 {7 - completed_days}일 더 완료하면 Perfect Week!")

    st.markdown("---")
    st.markdown("### ⏱ 타이머 공부 기록")
    study_time_record = st.session_state.get("study_time_record", {})
    today_study = study_time_record.get(str(today_date), 0)
    week_total = sum(study_time_record.get(d, 0) for d in week_days)
    week_days_studied = sum(1 for d in week_days if study_time_record.get(d, 0) > 0)
    week_avg = round(week_total / week_days_studied) if week_days_studied > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("오늘 공부", f"{today_study}분")
    with col2:
        st.metric("이번 주 총합", f"{week_total}분")
    with col3:
        st.metric("하루 평균", f"{week_avg}분")

    st.markdown("---")
    st.markdown("### 📖 과목별 공부 시간")
    subject_time2 = {}
    for task in st.session_state.tasks:
        if task["done"]:
            s = task["subject"]
            subject_time2[s] = subject_time2.get(s, 0) + task["duration"]

    if subject_time2:
        for subj, minutes in sorted(subject_time2.items(), key=lambda x: -x[1]):
            color = COLORS.get(subj, "#94A3B8")
            st.markdown(f"**{subj}** — {minutes}분")
            st.progress(minutes / max(subject_time2.values()))
    else:
        st.info("아직 완료한 할 일이 없어요!")

with tab4:
    st.markdown("### 🤖 AI 공부 조언")
    st.info("🔑 OpenAI API 키를 입력하면 AI 기능을 사용할 수 있어요!")

    api_key = st.text_input("OpenAI API 키 입력", type="password", placeholder="sk-...", key="api_key_input")
    question = st.text_area("궁금한 점을 입력하세요", placeholder="예: 오늘 공부 순서 추천해줘!", key="question_input")

    if st.button("🤖 AI에게 물어보기", use_container_width=True, key="btn_ask"):
        if not api_key:
            st.warning("API 키를 입력해주세요!")
        elif not question:
            st.warning("질문을 입력해주세요!")
        else:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                task_list = "\n".join([f"- [{t['subject']}] {t['title']} ({t['duration']}분, {'완료' if t['done'] else '미완료'})" for t in st.session_state.tasks])
                with st.spinner("AI가 답변 중이에요..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        max_tokens=1000,
                        messages=[
                            {"role": "system", "content": "너는 친근한 공부 도우미야. 짧고 실용적으로 한국어로 답해줘. 3~5문장 이내로."},
                            {"role": "user", "content": f"현재 할 일 목록:\n{task_list if task_list else '없음'}\n\n질문: {question}"}
                        ]
                    )
                st.success(response.choices[0].message.content)
            except Exception as e:
                st.error(f"오류: {e}")

    st.markdown("---")
    st.markdown("### ✨ AI 우선순위 자동 분류")

    if st.button("✨ 오늘 할 일 우선순위 분류", use_container_width=True, key="btn_priority"):
        if not api_key:
            st.warning("API 키를 입력해주세요!")
        else:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                today_undone = [t for t in today_tasks if not t["done"]]
                if not today_undone:
                    st.info("오늘 미완료 할 일이 없어요!")
                else:
                    task_list = "\n".join([f"{i+1}. [{t['subject']}] {t['title']} ({t['duration']}분)" for i, t in enumerate(today_undone)])
                    with st.spinner("AI가 분석 중이에요..."):
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            max_tokens=1000,
                            messages=[
                                {"role": "system", "content": "학생의 공부 우선순위를 정해주는 도우미야."},
                                {"role": "user", "content": f"할 일 목록:\n{task_list}\n\n각 항목에 🔴 높음 / 🟡 중간 / 🟢 낮음 으로 우선순위를 매기고 이유를 한 줄로 설명해줘."}
                            ]
                        )
                    st.success(response.choices[0].message.content)
            except Exception as e:
                st.error(f"오류: {e}")

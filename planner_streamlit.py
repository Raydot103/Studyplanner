import streamlit as st
import json
import datetime
import os

st.set_page_config(
    page_title="AI 공부 플래너",
    page_icon="📚",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap');
* { font-family: 'Noto Sans KR', sans-serif; }
.task-card {
    background: #1e293b;
    border-radius: 14px;
    padding: 14px 18px;
    margin: 8px 0;
    border-left: 4px solid;
}
.task-done { opacity: 0.5; text-decoration: line-through; }
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 6px;
}
.perfect-week {
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: white;
    padding: 16px;
    border-radius: 16px;
    text-align: center;
    font-size: 22px;
    font-weight: 900;
    margin: 12px 0;
}
</style>
""", unsafe_allow_html=True)

COLORS = {
    "수학": "#FF6B6B",
    "영어": "#4ECDC4",
    "국어": "#FFE66D",
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

st.markdown("# 📚 AI 공부 플래너")
st.markdown("---")

today = str(datetime.date.today())
today_tasks = [t for t in st.session_state.tasks if t["date"] == today]

done_count = sum(1 for t in today_tasks if t["done"])
total_count = len(today_tasks)

if total_count > 0:
    progress = done_count / total_count
    st.markdown(f"**오늘의 진행률** ({done_count}/{total_count} 완료)")
    st.progress(progress)
    if done_count == total_count:
        st.session_state.weekly_record[today] = True
        save_data()
        st.success("🎉 오늘 할 일을 모두 완료했어요!")
else:
    st.info("오늘 할 일을 추가해봐요!")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📋 오늘 할 일", "➕ 할 일 추가", "📊 주간 통계", "🤖 AI 조언"])

with tab1:
    if not today_tasks:
        st.markdown("오늘 할 일이 없어요. 추가해봐요!")

    for i, task in enumerate(st.session_state.tasks):
        if task["date"] != today:
            continue
        color = COLORS.get(task["subject"], "#94A3B8")
        done_class = "task-done" if task["done"] else ""
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
        with col1:
            checked = st.checkbox("", value=task["done"], key=f"check_{i}")
            if checked != task["done"]:
                st.session_state.tasks[i]["done"] = checked
                save_data()
                st.rerun()
        with col2:
            st.markdown(f"""
            <div class="task-card {done_class}" style="border-color: {color}">
                <span class="badge" style="background:{color}33; color:{color}">{task['subject']}</span>
                <strong>{task['title']}</strong>
                <span style="color:#64748b; font-size:13px"> ⏱ {task['duration']}분</span>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            if st.button("🗑", key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                save_data()
                st.rerun()

with tab2:
    st.markdown("### 새 할 일 추가")
    subject = st.selectbox("과목", list(COLORS.keys()))
    title = st.text_input("할 일")
    duration = st.number_input("예상 시간 (분)", min_value=5, max_value=300, step=5, value=30)
    if st.button("✅ 추가하기", use_container_width=True):
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
                color = "#334155"
            elif st.session_state.weekly_record.get(d):
                color = "#22c55e"
            else:
                color = "#ef4444"
            done = sum(1 for t in day_tasks if t["done"])
            total = len(day_tasks)
            st.markdown(f"""
            <div style="text-align:center">
                <div style="font-size:11px; color:#94a3b8; margin-bottom:4px">{name}</div>
                <div style="
                    background:{color};
                    height:80px;
                    border-radius:8px;
                    display:flex;
                    align-items:flex-end;
                    justify-content:center;
                    padding-bottom:6px;
                    font-size:11px;
                    color:white;
                    font-weight:700;
                ">{done}/{total}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"**이번 주 완료한 날: {completed_days} / 7일**")
    st.progress(completed_days / 7)

    if completed_days == 7:
        st.markdown('<div class="perfect-week">🏆 PERFECT WEEK! 대단해요!</div>', unsafe_allow_html=True)
    elif completed_days >= 5:
        st.success("🔥 거의 다 왔어요! 조금만 더!")
    else:
        st.info(f"💪 {7 - completed_days}일 더 완료하면 Perfect Week!")

    st.markdown("---")
    st.markdown("### 📖 과목별 공부 시간")
    subject_time = {}
    for task in st.session_state.tasks:
        if task["done"]:
            s = task["subject"]
            subject_time[s] = subject_time.get(s, 0) + task["duration"]

    if subject_time:
        for subject, minutes in sorted(subject_time.items(), key=lambda x: -x[1]):
            color = COLORS.get(subject, "#94A3B8")
            st.markdown(f"**{subject}** — {minutes}분")
            st.progress(minutes / max(subject_time.values()))
    else:
        st.info("아직 완료한 할 일이 없어요!")

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

with tab4:
    st.markdown("### 🤖 AI 공부 조언")
    st.info("🔑 API 키를 연결하면 AI 기능을 사용할 수 있어요!")

    api_key = st.text_input("Anthropic API 키 입력", type="password", placeholder="sk-ant-...")
    question = st.text_area("궁금한 점을 입력하세요", placeholder="예: 오늘 공부 순서 추천해줘!")
import streamlit as st
import json
import datetime
import os

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap');
* { font-family: 'Noto Sans KR', sans-serif; }
.perfect-week {
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: white;
    padding: 16px;
    border-radius: 16px;
    text-align: center;
    font-size: 22px;
    font-weight: 900;
    margin: 12px 0;
}
</style>
""", unsafe_allow_html=True)

COLORS = {
    "수학": "#FF6B6B",
    "영어": "#4ECDC4",
    "국어": "#FFE66D",
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

today = str(datetime.date.today())
today_tasks = [t for t in st.session_state.tasks if t["date"] == today]
done_count = sum(1 for t in today_tasks if t["done"])
total_count = len(today_tasks)

st.markdown("# 📚 AI Study Planner")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["⏱ 타이머", "📋 할 일", "📊 주간 통계", "🤖 AI 조언"])

# ── 탭1: 타이머 ──────────────────────────────────────────
with tab1:
    st.markdown("### 과목별 공부 비율")

    # 파이차트
    subject_time = {}
    for task in st.session_state.tasks:
        if task["done"]:
            s = task["subject"]
            subject_time[s] = subject_time.get(s, 0) + task["duration"]

    if subject_time:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.rcParams['font.family'] = 'DejaVu Sans'

        fig, ax = plt.subplots(figsize=(4, 4))
        fig.patch.set_facecolor('#0f1117')
        ax.set_facecolor('#0f1117')

        labels = list(subject_time.keys())
        sizes = list(subject_time.values())
        colors = [COLORS.get(s, "#94A3B8") for s in labels]

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.0f%%',
            startangle=90,
            textprops={'color': 'white', 'fontsize': 11}
        )
        for at in autotexts:
            at.set_color('white')

        st.pyplot(fig)
        plt.close()
    else:
        st.info("할 일을 완료하면 과목별 비율이 나와요!")

    st.markdown("---")
    st.markdown("### ⏱ 공부 타이머")

    timer_subject = st.selectbox("공부할 과목", list(COLORS.keys()), key="timer_sub")

    # 경과 시간 계산
    if st.session_state.timer_running and st.session_state.timer_start:
        elapsed = st.session_state.timer_elapsed + (datetime.datetime.now() - st.session_state.timer_start).seconds
    else:
        elapsed = st.session_state.timer_elapsed

    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60
    st.markdown(f"## 🕐 {hours:02d}:{minutes:02d}:{seconds:02d}")

    col1, col2, col3 = st.columns(3)

    with col1:
        if not st.session_state.timer_running:
            if st.button("▶ 시작", use_container_width=True):
                st.session_state.timer_running = True
                st.session_state.timer_start = datetime.datetime.now()
                st.session_state.timer_subject = timer_subject
                st.rerun()
        else:
            if st.button("⏸ 일시정지", use_container_width=True):
                elapsed_now = (datetime.datetime.now() - st.session_state.timer_start).seconds
                st.session_state.timer_elapsed += elapsed_now
                st.session_state.timer_running = False
                st.session_state.timer_start = None
                st.rerun()

    with col2:
        if st.button("⏹ 종료", use_container_width=True):
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
        if st.button("🔄 리셋", use_container_width=True):
            st.session_state.timer_running = False
            st.session_state.timer_start = None
            st.session_state.timer_elapsed = 0
            st.rerun()

    # 오늘 진행률
    st.markdown("---")
    st.markdown(f"**오늘 진행률: {done_count}/{total_count} 완료**")
    if total_count > 0:
        st.progress(done_count / total_count)
    else:
        st.progress(0)

# ── 탭2: 할 일 ───────────────────────────────────────────
with tab2:
    st.markdown("### 📋 오늘의 할 일")

    if not today_tasks:
        st.info("오늘 할 일이 없어요. 아래에서 추가해봐요!")

    for i, task in enumerate(st.session_state.tasks):
        if task["date"] != today:
            continue
        color = COLORS.get(task["subject"], "#94A3B8")
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
        with col1:
            checked = st.checkbox("", value=task["done"], key=f"check_{i}")
            if checked != task["done"]:
                st.session_state.tasks[i]["done"] = checked
                if all(t["done"] for t in today_tasks):
                    st.session_state.weekly_record[today] = True
                save_data()
                st.rerun()
        with col2:
            done_style = "opacity:0.5; text-decoration:line-through;" if task["done"] else ""
            st.markdown(f"""
            <div style="background:#1e293b; border-radius:12px; padding:12px 16px;
                        margin:4px 0; border-left:4px solid {color}; {done_style}">
                <span style="background:{color}33; color:{color}; padding:2px 8px;
                             border-radius:20px; font-size:12px; font-weight:600;">
                    {task['subject']}
                </span>
                <strong style="margin-left:8px">{task['title']}</strong>
                <span style="color:#64748b; font-size:12px"> ⏱ {task['duration']}분</span>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            if st.button("🗑", key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                save_data()
                st.rerun()

    st.markdown("---")
    st.markdown("### ➕ 할 일 추가")
    subject = st.selectbox("과목", list(COLORS.keys()), key="add_sub")
    title = st.text_input("할 일 내용")
    duration = st.number_input("예상 시간 (분)", min_value=5, max_value=300, step=5, value=30)

    if st.button("✅ 추가하기", use_container_width=True):
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

# ── 탭3: 주간 통계 ───────────────────────────────────────
with tab3:
    st.markdown("### 📊 주간 통계")

    today_date = datetime.date.today()
    monday = today_date - datetime.timedelta(days=today_date.weekday())
    week_days = [(monday + datetime.timedelta(days=i)).isoformat() for i in range(7)]
    day_names = ["월", "화", "수", "목", "금", "토", "일"]
    completed_days = sum(1 for d in week_days if st.session_state.weekly_record.get(d))

    # 요일별 막대
    st.markdown("#### 이번 주 일과 현황")
    cols = st.columns(7)
    for i, (col, d, name) in enumerate(zip(cols, week_days, day_names)):
        with col:
            day_tasks = [t for t in st.session_state.tasks if t["date"] == d]
            if not day_tasks:
                color = "#334155"
            elif st.session_state.weekly_record.get(d):
                color = "#22c55e"
            else:
                color = "#ef4444"
            done = sum(1 for t in day_tasks if t["done"])
            total = len(day_tasks)
            st.markdown(f"""
            <div style="text-align:center">
                <div style="font-size:11px; color:#94a3b8; margin-bottom:4px">{name}</div>
                <div style="background:{color}; height:80px; border-radius:8px;
                            display:flex; align-items:flex-end; justify-content:center;
                            padding-bottom:6px; font-size:11px; color:white; font-weight:700;">
                    {done}/{total}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
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
    subject_time = {}
    for task in st.session_state.tasks:
        if task["done"]:
            s = task["subject"]
            subject_time[s] = subject_time.get(s, 0) + task["duration"]

    if subject_time:
        for subject, minutes in sorted(subject_time.items(), key=lambda x: -x[1]):
            color = COLORS.get(subject, "#94A3B8")
            st.markdown(f"**{subject}** — {minutes}분")
            st.progress(minutes / max(subject_time.values()))
    else:
        st.info("아직 완료한 할 일이 없어요!")

# ── 탭4: AI 조언 ─────────────────────────────────────────
with tab4:
    st.markdown("### 🤖 AI 공부 조언")
    st.info("🔑 API 키를 연결하면 AI 기능을 사용할 수 있어요!")

    api_key = st.text_input("Anthropic API 키 입력", type="password", placeholder="sk-ant-...")
    question = st.text_area("궁금한 점을 입력하세요", placeholder="예: 오늘 공부 순서 추천해줘!")

    if st.button("🤖 AI에게 물어보기", use_container_width=True):
        if not api_key:
            st.warning("API 키를 입력해주세요!")
        elif not question:
            st.warning("질문을 입력해주세요!")
        else:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                task_list = "\n".join([f"- [{t['subject']}] {t['title']} ({t['duration']}분, {'완료' if t['done'] else '미완료'})" for t in st.session_state.tasks])
                with st.spinner("AI가 답변 중이에요..."):
                    message = client.messages.create(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=1000,
                        messages=[{"role": "user", "content": f"""너는 친근한 공부 도우미야.

현재 할 일 목록:
{task_list if task_list else '없음'}

질문: {question}

짧고 실용적으로 한국어로 답해줘. 3~5문장 이내로."""}]
                    )
                st.success(message.content[0].text)
            except Exception as e:
                st.error(f"오류: {e}")

    st.markdown("---")
    st.markdown("### ✨ AI 우선순위 자동 분류")

    if st.button("✨ 오늘 할 일 우선순위 분류", use_container_width=True):
        if not api_key:
            st.warning("API 키를 입력해주세요!")
        else:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                today_undone = [t for t in today_tasks if not t["done"]]
                if not today_undone:
                    st.info("오늘 미완료 할 일이 없어요!")
                else:
                    task_list = "\n".join([f"{i+1}. [{t['subject']}] {t['title']} ({t['duration']}분)" for i, t in enumerate(today_undone)])
                    with st.spinner("AI가 분석 중이에요..."):
                        message = client.messages.create(
                            model="claude-haiku-4-5-20251001",
                            max_tokens=1000,
                            messages=[{"role": "user", "content": f"""학생의 오늘 할 일 목록을 보고 우선순위를 정해줘.

할 일 목록:
{task_list}

각 항목에 🔴 높음 / 🟡 중간 / 🟢 낮음 으로 우선순위를 매기고 이유를 한 줄로 설명해줘."""}]
                        )
                    st.success(message.content[0].text)
            except Exception as e:
                st.error(f"오류: {e}")

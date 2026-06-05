import datetime
import time

tasks = []
weekly_record = {}
study_time_record = {}

def add_task():
  while True:
    print("\n-- 할 일 추가 --")
    subject = input("과목: ")
    title = input("할 일: ")
    duration = int(input("예상 시간(분): "))
    task = {
      "subject": subject,
      "title": title,
      "duration": duration,
      "done": False,
      "date": str(datetime.date.today())
    }
    tasks.append(task)
    print(f"✅ 추가됨: [{subject}] {title}")
    more = input("\n계속 추가할까요? (y/n): ")
    if more.lower() != "y":
      break

def show_tasks():
  today = str(datetime.date.today())
  today_tasks = [t for t in tasks if t["date"] == today]
  if not today_tasks:
    print("\n오늘 할 일이 없어요!")
    return
  print("\n📋 오늘의 할 일:")
  for i, task in enumerate(today_tasks):
    status = "✅" if task["done"] else "⬜"
    print(f"{i+1}. {status} [{task['subject']}] {task['title']} ({task['duration']}분)")

def complete_task():
  show_tasks()
  number = int(input("\n완료할 번호: "))
  today = str(datetime.date.today())
  today_tasks = [t for t in tasks if t["date"] == today]
  if 1 <= number <= len(today_tasks):
    today_tasks[number-1]["done"] = True
    print(f"✅ 완료: {today_tasks[number-1]['title']}")
    check_perfect_day()
  else:
    print("없는 번호예요!")

def delete_task():
  show_tasks()
  number = int(input("\n삭제할 번호: "))
  today = str(datetime.date.today())
  today_tasks = [t for t in tasks if t["date"] == today]
  if 1 <= number <= len(today_tasks):
    removed = today_tasks[number-1]
    tasks.remove(removed)
    print(f"🗑 삭제됨: {removed['title']}")
  else:
    print("없는 번호예요!")

def check_perfect_day():
  today = str(datetime.date.today())
  today_tasks = [t for t in tasks if t["date"] == today]
  if today_tasks and all(t["done"] for t in today_tasks):
    weekly_record[today] = True
    print("🎉 오늘 할 일을 모두 완료했어요!")
    check_perfect_week()
  else:
    done = sum(1 for t in today_tasks if t["done"])
    total = len(today_tasks)
    print(f"📋 오늘 진행상황: {done}/{total} 완료")

def check_perfect_week():
  today = datetime.date.today()
  monday = today - datetime.timedelta(days=today.weekday())
  week_days = [(monday + datetime.timedelta(days=i)).isoformat() for i in range(7)]
  completed_days = sum(1 for d in week_days if weekly_record.get(d))
  print(f"\n📊 이번 주 완료한 날: {completed_days}/7일")
  if completed_days == 7:
    print("🏆 PERFECT WEEK! 대단해요!")
  elif completed_days >= 5:
    print("🔥 거의 다 왔어요! 조금만 더!")
  else:
    print(f"💪 {7 - completed_days}일 더 완료하면 Perfect Week!")

def study_timer():
  print("\n⏱ 공부 타이머 시작!")
  print("엔터를 눌러 시작하세요...")
  input()
  total_seconds = 0
  print("✅ 타이머 시작! (p: 일시정지 / q: 종료)")
  while True:
    start = time.time()
    cmd = input()
    elapsed = time.time() - start
    total_seconds += elapsed
    mins = int(total_seconds // 60)
    secs = int(total_seconds % 60)
    print(f"⏱ 현재 {mins:02d}:{secs:02d}")
    if cmd.lower() == "p":
      print("⏸ 일시정지. 재개하려면 엔터...")
      input()
      print("▶ 재개! (p: 일시정지 / q: 종료)")
    elif cmd.lower() == "q":
      break
  total_mins = round(total_seconds / 60)
  today = str(datetime.date.today())
  study_time_record[today] = study_time_record.get(today, 0) + total_mins
  print(f"\n🎉 공부 완료! 총 {total_mins}분 공부했어요!")

def weekly_stats():
  print("\n📊 주간 통계")
  today = datetime.date.today()
  monday = today - datetime.timedelta(days=today.weekday())
  week_days = [(monday + datetime.timedelta(days=i)).isoformat() for i in range(7)]
  subject_time = {}
  for task in tasks:
    if task["done"]:
      s = task["subject"]
      subject_time[s] = subject_time.get(s, 0) + task["duration"]
  if subject_time:
    print("\n📖 과목별 완료 시간:")
    for subject, minutes in sorted(subject_time.items(), key=lambda x: -x[1]):
      print(f"  {subject}: {minutes}분")
  else:
    print("아직 완료한 할 일이 없어요!")
  print("\n⏱ 타이머 공부 기록:")
  today_study = study_time_record.get(str(today), 0)
  week_total = sum(study_time_record.get(d, 0) for d in week_days)
  week_days_studied = sum(1 for d in week_days if study_time_record.get(d, 0) > 0)
  week_avg = round(week_total / week_days_studied) if week_days_studied > 0 else 0
  print(f"  오늘 공부 시간: {today_study}분")
  print(f"  이번 주 총 공부 시간: {week_total}분")
  print(f"  이번 주 하루 평균: {week_avg}분")
  check_perfect_week()

def ai_advice():
  print("\n🤖 AI 공부 조언 (준비 중)")

def ai_priority():
  print("\n🤖 AI 우선순위 분류 (준비 중)")

def menu():
  print("\n" + "="*30)
  print("📚 AI 공부 플래너")
  print("="*30)
  print("1. 할 일 추가")
  print("2. 할 일 목록 보기")
  print("3. 완료 체크")
  print("4. 할 일 삭제")
  print("5. AI 공부 조언")
  print("6. AI 우선순위 분류")
  print("7. 주간 통계")
  print("8. 공부 타이머")
  print("9. 종료")
  print("="*30)

while True:
  menu()
  choice = input("선택: ")
  if choice == "1":
    add_task()
  elif choice == "2":
    show_tasks()
  elif choice == "3":
    complete_task()
  elif choice == "4":
    delete_task()
  elif choice == "5":
    ai_advice()
  elif choice == "6":
    ai_priority()
  elif choice == "7":
    weekly_stats()
  elif choice == "8":
    study_timer()
  elif choice == "9":
    print("👋 종료!")
    break
  else:
    print("잘못된 선택이에요!")

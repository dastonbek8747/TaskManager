import streamlit as st
import pandas as pd
from datetime import date
from main import TaskManager, Priority

st.set_page_config(page_title="Vazifalar", page_icon="📋", layout="centered")

if "mgr" not in st.session_state:
    st.session_state.mgr = TaskManager()

mgr: TaskManager = st.session_state.mgr

COLORS = {"Yuqori": "🔴", "O'rta": "🟡", "Past": "🟢"}

st.title("📋 Vazifalar")

page = st.sidebar.radio("", ["Ro'yxat", "Qo'shish", "Statistika"])

if page == "Ro'yxat":
    stats = mgr.stats()
    c1, c2, c3 = st.columns(3)
    c1.metric("Jami", stats["total"])
    c2.metric("Bajarildi", stats["done"])
    c3.metric("Kechikdi", stats["overdue"])

    if mgr.tasks:
        st.progress(stats["done"] / stats["total"] if stats["total"] else 0)

    st.divider()

    overdue_ids = {t.id for t, _ in mgr.overdue_tasks()}
    rows = [
        {
            "Vazifa":      t.title,
            "Deadline":    str(t.deadline),
            "Ustuvorlik":  COLORS[t.priority.value] + " " + t.priority.value,
            "Status":      "✅" if t.status else ("🔴 Kechikdi" if t.id in overdue_ids else "⏳ Faol"),
            "_id":         str(t.id),
        }
        for t in mgr.tasks
    ]

    if not rows:
        st.info("Hali vazifa yo'q.")
    else:
        st.dataframe(
            pd.DataFrame(rows).drop(columns=["_id"]),
            use_container_width=True,
            hide_index=True,
        )

        st.divider()
        options = {f"{t.title}": t.id for t in mgr.tasks}
        selected = st.selectbox("Vazifa tanlang", list(options.keys()))
        task_id  = options[selected]

        col1, col2 = st.columns(2)
        if col1.button("✅ Bajarildi", use_container_width=True):
            res = mgr.complete_task(task_id)
            (st.success if res["ok"] else st.error)(res["message"])
            st.rerun()
        if col2.button("🗑️ O'chirish", use_container_width=True):
            res = mgr.delete_task(task_id)
            (st.success if res["ok"] else st.error)(res["message"])
            st.rerun()

elif page == "Qo'shish":
    st.subheader("Yangi vazifa")
    with st.form("form", clear_on_submit=True):
        title    = st.text_input("Vazifa nomi")
        deadline = st.date_input("Deadline", min_value=date.today())
        priority = st.selectbox("Ustuvorlik", [p.value for p in Priority])
        ok = st.form_submit_button("Qo'shish", use_container_width=True, type="primary")

    if ok:
        if not title.strip():
            st.error("Nom bo'sh bo'lmasin!")
        else:
            mgr.add_task(title.strip(), deadline, Priority(priority))
            st.success(f"**{title}** qo'shildi!")
            st.balloons()

elif page == "Statistika":
    st.subheader("Statistika")
    stats = mgr.stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jami",      stats["total"])
    c2.metric("Bajarildi", stats["done"])
    c3.metric("Faol",      stats["active"])
    c4.metric("Kechikdi",  stats["overdue"])

    if mgr.tasks:
        st.divider()
        pri_data = {p.value: len(list(mgr.filter_by_priority(p))) for p in Priority}
        st.bar_chart(pri_data)
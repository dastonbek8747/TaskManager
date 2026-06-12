import streamlit as st

if "user_autentifaktsiya" not in st.session_state:
    st.session_state.user_autentifaktsiya = True

if not st.session_state.user_autentifaktsiya:
    tab1, tab2 = st.tabs(["Saytga Kirish", "Ro'yhatdan o'tish"])

    with tab1:
        st.header("Saytga Kirish")
        username = st.text_input("username")
        password = st.text_input("password")
        button = st.button("Kirish")

    with tab2:
        st.header("Ro'yhatdan o'tish")

        username_register = st.text_input("username", key="username_register")
        email_register = st.text_input("Email", key="email_register")
        password_register = st.text_input("password", key="password_register")
        button = st.button("Ro'yhatdan o'tish", key="button")

else:

    with st.sidebar.header("Bugungi  Vazifalar"):
        yuqori, orta, past = st.sidebar.tabs(["Yuqori", "O'rta", "Past"])
        with yuqori:
            st.header("Yuqori darajadagi vazifalar")
        with orta:
            st.header("O'rta darajagi vazifalar")
        with past:
            st.header("Past darajagi vazifalar")

    tab1, tab2,tab3 = st.tabs(["Vazifa qoshish", "Vazifani o'chirish","Muddati tugagan vazifalar"])
    with tab1:
        st.header("Bugun uchun yangi vazifalar")
        task_title = st.text_input("Vazifa nomi")
        topshirish_muddati = st.date_input("Topshirish vaqti ")
        task_ustuvorligi = st.selectbox("Vazifa ustuvorligi", ("Yuqori", "O'rta", "Past"))
        task_status = st.selectbox("Vazifa bajarilganligi", ("Bajarilmadi", "Bajarildi"))

        vazifa_submit_btn = st.button("Vazifani qo'shish")
        if vazifa_submit_btn:
            st.snow()
    with tab2:
        kechagi, bugungi, oldingilari = st.tabs(["Kechagi", "Bugungi", "Oldingilari"])
        with kechagi:
            st.header("Mavjud vazifalar")
            for i in range(10):
                st.checkbox(f"Vazifa nomalari chiqib keladi {i}")
    with tab3:
        st.header("Mavjud vazifalar")
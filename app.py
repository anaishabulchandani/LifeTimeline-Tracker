import streamlit as st
import mysql.connector
import pandas as pd

# DB connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anaisha_27",
    database="life_timeline"
)
cursor = db.cursor()

st.title("Life Timeline Dashboard")

#  ADD EVENT 
st.subheader("Add Event")

col1, col2 = st.columns(2)

with col1:
    title = st.text_input("Title")
    description = st.text_input("Description")

with col2:
    date = st.date_input("Date")
    mood = st.slider("Mood (1-5)", 1, 5)

if st.button("Add Event"):
    cursor.execute(
        "INSERT INTO Events (user_id, title, description, event_date, event_type, mood_rating) VALUES (%s, %s, %s, %s, %s, %s)",
        (1, title, description, date, 'general', mood)
    )
    db.commit()
    st.success("Event Added!")

#  FILTERS 
st.subheader("Filter Events")

min_mood = st.slider("Minimum Mood", 1, 5, 1)

cursor.execute("SELECT * FROM Events WHERE mood_rating >= %s", (min_mood,))
events = cursor.fetchall()

#  VIEW EVENTS 
st.subheader("All Events")

for e in events:
    col1, col2 = st.columns([4,1])

    with col1:
        st.write(f"**{e[2]}** | {e[4]} |  Mood: {e[6]}")

    with col2:
        if st.button("❌", key=e[0]):
            cursor.execute("DELETE FROM Events WHERE event_id=%s", (e[0],))
            db.commit()
            st.experimental_rerun()

#  ANALYSIS 
st.subheader(" Monthly Analysis")

cursor.execute("SELECT MONTH(event_date), COUNT(*) FROM Events GROUP BY MONTH(event_date)")
data = cursor.fetchall()

df = pd.DataFrame(data, columns=["Month", "Events"])

st.bar_chart(df.set_index("Month"))

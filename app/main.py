import streamlit as st
import pandas as pd
from bandit_model import EpsilonGreedyBandit

# Initialize state
if "bandit" not in st.session_state:
    st.session_state.bandit = EpsilonGreedyBandit(arms=["Combo A", "Combo B"], epsilon=0.1)
    st.session_state.shown_counts = {"Combo A": 0, "Combo B": 0}
    st.session_state.click_counts = {"Combo A": 0, "Combo B": 0}

st.title("BeanBoost A/B Testing Simulator")
st.markdown("Click a combo to simulate a customer choosing it. The model learns which one works best based on actual choices.")

# Choose next recommendation
next_recommendation = st.session_state.bandit.choose_arm()
st.session_state.shown_counts[next_recommendation] += 1

st.markdown(f"### 🤖 The model recommends: **{next_recommendation}**")

col1, col2 = st.columns(2)

with col1:
    if st.button("Customer Chooses Combo A"):
        st.session_state.bandit.update("Combo A", reward=1)
        st.session_state.click_counts["Combo A"] += 1

with col2:
    if st.button("Customer Chooses Combo B"):
        st.session_state.bandit.update("Combo B", reward=1)
        st.session_state.click_counts["Combo B"] += 1

# Show updated stats
df = pd.DataFrame({
    "Combo": ["Combo A", "Combo B"],
    "Times Shown": [st.session_state.shown_counts["Combo A"], st.session_state.shown_counts["Combo B"]],
    "Times Chosen": [st.session_state.click_counts["Combo A"], st.session_state.click_counts["Combo B"]],
    "Estimated Success Rate": [
        f"{(st.session_state.click_counts['Combo A'] / st.session_state.shown_counts['Combo A'] * 100):.1f}%" 
        if st.session_state.shown_counts["Combo A"] > 0 else "N/A",
        f"{(st.session_state.click_counts['Combo B'] / st.session_state.shown_counts['Combo B'] * 100):.1f}%" 
        if st.session_state.shown_counts["Combo B"] > 0 else "N/A"
    ]
})

st.markdown("### 📊 Performance Overview")
st.table(df)

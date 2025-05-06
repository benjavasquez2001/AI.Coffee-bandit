import streamlit as st
import pandas as pd

from models.bandit_model import EpsilonGreedyBandit


# Initialize session state for bandit model and results
if "bandit" not in st.session_state:
    st.session_state.bandit = EpsilonGreedyBandit(arms=["Combo A", "Combo B"], epsilon=0.1)
    st.session_state.history = []

st.title("BeanBoost A/B Testing Simulator")
st.markdown("Click on a combo to simulate a customer choosing it. The model will learn which performs best over time.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Customer Chooses Combo A"):
        st.session_state.bandit.update("Combo A", reward=1)
        st.session_state.history.append(("Combo A", 1))

with col2:
    if st.button("Customer Chooses Combo B"):
        st.session_state.bandit.update("Combo B", reward=1)
        st.session_state.history.append(("Combo B", 1))

# Show model decision logic
next_recommendation = st.session_state.bandit.choose_arm()
st.markdown(f"### 🤖 The model recommends: **{next_recommendation}**")

# Show stats
stats = st.session_state.bandit.get_stats()
df_stats = pd.DataFrame({
    "Combo": list(stats["counts"].keys()),
    "Times Shown": list(stats["counts"].values()),
    "Estimated Success Rate": [f"{v:.2%}" for v in stats["values"].values()]
})
st.table(df_stats)

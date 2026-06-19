import streamlit as st
import json
from pathlib import Path

# ---------- PATH HELPERS ----------

BASE_DIR = Path(__file__).parent  # folder where app.py lives

def load_questions(unit_name: str):
    # Path works both locally and on Streamlit Cloud
    data_path = BASE_DIR / "data" / f"{unit_name}.json"

    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)
# ---------- UNIT 1: DEMOGRAPHIC CYCLE ----------

QUESTIONS_U1 = load_questions("unit1")

STAGE_HINTS_U1 = {
    "U1_S1": "Think of very old, pre‑industrial societies: many babies born, many people die early, so population hardly grows.",
    "U1_S2": "Imagine vaccines and clean water arrive: deaths fall fast, but families still have many children, so population explodes.",
    "U1_S3": "Now picture urban, educated families: fewer children per family, deaths low, population still rising but slope is less steep.",
    "U1_S4": "Finally, advanced countries: small families, long life expectancy, total population high and roughly stable."
}

# ---------- UNIT 2: DEMOGRAPHIC INDICATORS (AGR) ----------

QUESTIONS_U2 = load_questions("unit2_agr")

HINTS_U2 = {
    "core": "AGR ≈ (CBR − CDR) / 10 when CBR and CDR are per 1000. Think: difference in rates, then divide by 10 to get % per year."
}

def get_u2_cue(question_id: str) -> str:
    if question_id == "U2_AGR_Q1":
        return "Cue: Subtract CDR from CBR, then divide by 10."
    if question_id == "U2_AGR_Q2":
        return "Cue: First calculate AGR, then map it to the growth category."
    if question_id == "U2_AGR_Q3":
        return "Cue: Remember ~2% AGR is considered very rapid / explosive."
    if question_id == "U2_AGR_Q4":
        return "Cue: Larger (CBR − CDR) means higher AGR."
    return ""

# ---------- RESET HELPERS ----------

def reset_unit1_state():
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_answers = {}
    st.session_state.run_id = 0
    st.session_state.finished = False
    st.session_state.hint_shown = False

def reset_unit2_state():
    st.session_state.current_q_u2 = 0
    st.session_state.score_u2 = 0
    st.session_state.answered_u2 = False
    st.session_state.selected_answers_u2 = {}
    st.session_state.run_id_u2 = 0
    st.session_state.finished_u2 = False

# ---------- INITIAL GLOBAL STATE ----------

if "page" not in st.session_state:
    st.session_state.page = "home"  # "home", "unit1", "unit2"

# Unit 1 state
for key, default in [
    ("current_q", 0),
    ("score", 0),
    ("answered", False),
    ("selected_answers", {}),
    ("run_id", 0),
    ("finished", False),
    ("hint_shown", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# Unit 2 state
for key, default in [
    ("current_q_u2", 0),
    ("score_u2", 0),
    ("answered_u2", False),
    ("selected_answers_u2", {}),
    ("run_id_u2", 0),
    ("finished_u2", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ---------- HOME PAGE ----------

def render_home():
    st.title("PSM Learning App")
    st.write("Short, addictive chunks for Community Medicine.")
    st.markdown("---")
    st.subheader("Pick a unit to start")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Unit 1")
        st.write("Demographic cycle (Stages 1–4)")
        if st.button("Start Unit 1", use_container_width=True):
            reset_unit1_state()
            st.session_state.page = "unit1"
            st.rerun()

    with col2:
        st.markdown("#### Unit 2")
        st.write("Demographic indicators (Annual Growth Rate)")
        if st.button("Start Unit 2", use_container_width=True):
            reset_unit2_state()
            st.session_state.page = "unit2"
            st.rerun()

    st.markdown("---")
    st.caption("Tip: Finish a unit once, then replay quickly to strengthen recall.")

# ---------- UNIT 1 PAGE ----------

def render_unit1():
    if st.session_state.finished:
        total_q = len(QUESTIONS_U1)
        score = st.session_state.score
        percent = round(score * 100 / total_q)

        st.title("Unit 1 – Demographic cycle")

        col_score, col_actions = st.columns([2, 1])
        with col_score:
            st.subheader("Your performance")
            st.write(f"Correct: **{score} / {total_q}**")
            st.write(f"Score: **{percent}%**")
            if percent >= 80:
                st.success("Excellent! You have a strong grasp of the demographic cycle.")
            elif percent >= 50:
                st.info("Good start. One more quick run will lock in the ideas.")
            else:
                st.warning("Needs revision. Replay focusing on where you missed questions.")

        with col_actions:
            st.markdown("#### Next steps")
            if st.button("Restart Unit 1", use_container_width=True):
                reset_unit1_state()
                st.rerun()
            if st.button("Back to home", use_container_width=True):
                reset_unit1_state()
                st.session_state.page = "home"
                st.rerun()

        st.markdown("---")
        st.subheader("Full concept recap: Demographic cycle (Stages 1–4)")

        st.markdown(
            "- The demographic cycle describes how a country's population changes over time as it develops.\n"
            "- It tracks **birth rate (BR)** and **death rate (DR)** and how the gap between them affects population size."
        )

        st.markdown("**Stage 1 – High stationary**")
        st.markdown(
            "- BR: High; DR: High.\n"
            "- Population size: Almost stable, very slow growth.\n"
            "- Typical of pre‑industrial societies with poor sanitation, frequent infections, famines."
        )

        st.markdown("**Stage 2 – Early expanding**")
        st.markdown(
            "- BR: Still high; DR: Falls rapidly due to better food, sanitation, and basic public health.\n"
            "- Population size: Rises very quickly because births greatly exceed deaths.\n"
            "- Seen in developing countries entering early modernization."
        )

        st.markdown("**Stage 3 – Late expanding**")
        st.markdown(
            "- BR: Starts to fall as families choose fewer children; DR: Low and stable.\n"
            "- Population size: Still increasing, but more slowly than Stage 2.\n"
            "- Linked to urbanization, female education, contraception, and higher cost of raising children."
        )

        st.markdown("**Stage 4 – Low stationary**")
        st.markdown(
            "- BR: Low; DR: Low.\n"
            "- Population size: High and roughly stable.\n"
            "- Typical of developed countries with small families and long life expectancy."
        )

        st.stop()

    st.title("Unit 1 – Demographic cycle")
    st.caption("Mode: Learn & quiz · ~2 minutes")
    st.progress((st.session_state.current_q + 1) / len(QUESTIONS_U1))

    q = QUESTIONS_U1[st.session_state.current_q]

    hint_key = None
    if q["id"].startswith("U1_S1"):
        hint_key = "U1_S1"
    elif q["id"].startswith("U1_S2"):
        hint_key = "U1_S2"
    elif q["id"].startswith("U1_S3"):
        hint_key = "U1_S3"
    elif q["id"].startswith("U1_S4"):
        hint_key = "U1_S4"

    with st.container():
        st.markdown(
            """
            <div style="padding: 1rem; border-radius: 10px; background-color: #f9fafb; border: 1px solid #e5e7eb;">
            """,
            unsafe_allow_html=True,
        )

        st.subheader(f"Item {st.session_state.current_q + 1} of {len(QUESTIONS_U1)}")

        if not st.session_state.hint_shown:
            if hint_key:
                st.info(STAGE_HINTS_U1[hint_key])
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Got it, show question"):
                    st.session_state.hint_shown = True
                    st.rerun()
            with col2:
                if st.button("Back to home"):
                    reset_unit1_state()
                    st.session_state.page = "home"
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            st.stop()

        st.write(q["question"])

        radio_key = f"u1_radio_{st.session_state.run_id}"

        user_answer = st.radio(
            "Choose one:",
            q["options"],
            index=None,
            key=radio_key,
            disabled=st.session_state.answered
        )

        if not st.session_state.answered:
            if st.button("Submit"):
                if user_answer is None or user_answer == "":
                    st.warning("Please select an option before submitting.")
                else:
                    st.session_state.answered = True
                    st.session_state.selected_answers[q["id"]] = user_answer
                    correct_option = q["options"][q["correct_index"]]
                    if user_answer == correct_option:
                        st.success("Correct ✅")
                        st.session_state.score += 1
                    else:
                        st.error(f"Wrong ❌ (Correct: {correct_option})")
                    st.info(q["explanation"])

        if st.session_state.answered:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Next"):
                    st.session_state.answered = False
                    st.session_state.current_q += 1
                    st.session_state.hint_shown = False
                    if st.session_state.current_q >= len(QUESTIONS_U1):
                        st.session_state.finished = True
                    st.session_state.run_id += 1
                    st.rerun()
            with col2:
                if st.button("Back to home"):
                    reset_unit1_state()
                    st.session_state.page = "home"
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.write(f"Score so far: {st.session_state.score} / {len(QUESTIONS_U1)}")

# ---------- UNIT 2 PAGE ----------

def render_unit2():
    if st.session_state.finished_u2:
        total_q = len(QUESTIONS_U2)
        score = st.session_state.score_u2
        percent = round(score * 100 / total_q)

        st.title("Unit 2 – Demographic indicators (AGR)")

        col_score, col_actions = st.columns([2, 1])
        with col_score:
            st.subheader("Your performance")
            st.write(f"Correct: **{score} / {total_q}**")
            st.write(f"Score: **{percent}%**")
            if percent >= 80:
                st.success("Excellent! AGR calculation and interpretation are solid.")
            elif percent >= 50:
                st.info("Good start. One more run will make AGR feel automatic.")
            else:
                st.warning("Needs revision. Replay focusing on calculation steps.")

        with col_actions:
            st.markdown("#### Next steps")
            if st.button("Restart Unit 2", use_container_width=True):
                reset_unit2_state()
                st.rerun()
            if st.button("Back to home", use_container_width=True):
                reset_unit2_state()
                st.session_state.page = "home"
                st.rerun()

        st.markdown("---")
        st.subheader("Full concept recap: Annual Growth Rate (AGR)")

        st.markdown(
            "- Crude birth rate (CBR) and crude death rate (CDR) are usually given per 1000 population.\n"
            "- Annual growth rate (AGR) is approximated as **(CBR − CDR) / 10**, giving percentage growth per year."
        )

        st.markdown("**AGR categories (typical ranges)**")
        st.markdown(
            "- Slow growing: around 0.5%.\n"
            "- Moderate growing: about 0.5–1%.\n"
            "- Rapid growing: about 1–1.5%.\n"
            "- Very rapid / explosive: ≥ 2%."
        )

        st.markdown(
            "- Example: CBR 30, CDR 10 → AGR = (30 − 10)/10 = 2% → very rapid / explosive.\n"
            "- Example: CBR 25, CDR 20 → AGR = (25 − 20)/10 = 0.5% → slow growth."
        )

        st.stop()

    st.title("Unit 2 – Demographic indicators (AGR)")
    st.caption("Mode: Learn & quiz · ~2 minutes")
    st.progress((st.session_state.current_q_u2 + 1) / len(QUESTIONS_U2))

    st.info(HINTS_U2["core"])

    q = QUESTIONS_U2[st.session_state.current_q_u2]

    with st.container():
        st.markdown(
            """
            <div style="padding: 1rem; border-radius: 10px; background-color: #f9fafb; border: 1px solid #e5e7eb;">
            """,
            unsafe_allow_html=True,
        )

        st.subheader(f"Item {st.session_state.current_q_u2 + 1} of {len(QUESTIONS_U2)}")

        cue = get_u2_cue(q["id"])
        if cue:
            st.caption(cue)

        st.write(q["question"])

        radio_key = f"u2_radio_{st.session_state.run_id_u2}"

        user_answer = st.radio(
            "Choose one:",
            q["options"],
            index=None,
            key=radio_key,
            disabled=st.session_state.answered_u2
        )

        if not st.session_state.answered_u2:
            if st.button("Submit"):
                if user_answer is None or user_answer == "":
                    st.warning("Please select an option before submitting.")
                else:
                    st.session_state.answered_u2 = True
                    st.session_state.selected_answers_u2[q["id"]] = user_answer
                    correct_option = q["options"][q["correct_index"]]
                    if user_answer == correct_option:
                        st.success("Correct ✅")
                        st.session_state.score_u2 += 1
                    else:
                        st.error(f"Wrong ❌ (Correct: {correct_option})")
                    st.info(q["explanation"])

        if st.session_state.answered_u2:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Next"):
                    st.session_state.answered_u2 = False
                    st.session_state.current_q_u2 += 1
                    if st.session_state.current_q_u2 >= len(QUESTIONS_U2):
                        st.session_state.finished_u2 = True
                    st.session_state.run_id_u2 += 1
                    st.rerun()
            with col2:
                if st.button("Back to home"):
                    reset_unit2_state()
                    st.session_state.page = "home"
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.write(f"Score so far: {st.session_state.score_u2} / {len(QUESTIONS_U2)}")

# ---------- ROUTER ----------

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "unit1":
    render_unit1()
elif st.session_state.page == "unit2":
    render_unit2()

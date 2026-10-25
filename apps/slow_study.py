import streamlit as st
from toolkit.local_ai import generate, health_check
from toolkit.ui import configure_page, footer

configure_page(
    "SlowStudy", "▤",
    "Convert your own course material into revision notes, flashcards, and practice questions — without the busywork.",
)

with st.container(border=True):
    st.markdown('<div class="section-label">01 / Study material</div>', unsafe_allow_html=True)
    notes = st.text_area(
        "Course notes", height=250, key="study_input",
        placeholder="Paste course notes or a topic here. For the most grounded results, use specific notes from your course.",
        label_visibility="collapsed",
    )
    a, b, c = st.columns([1, 1.2, 1])
    with a:
        level = st.selectbox("Learning level", ["Beginner", "High school", "University"], index=2)
    with b:
        kind = st.selectbox("Study format", ["Revision summary", "Flashcards", "Practice questions"])
    with c:
        count = st.selectbox("Items", [3, 5, 8, 10], index=1, disabled=(kind == "Revision summary"))
    st.caption(f"{len(notes):,} characters · max 16,000")
    submitted = st.button("Create study set", type="primary", disabled=not notes.strip(), use_container_width=True)

if submitted:
    if kind == "Revision summary":
        task = "Write a structured revision summary, key terms, and a short self-check with answers."
    elif kind == "Flashcards":
        task = f"Create exactly {count} concise flashcards. Format each with a clear Q: and A:. One factual question per card. Avoid redundant cards."
    else:
        task = f"Create exactly {count} practice questions appropriate for the level. Include the correct answer and a short explanation. Mix conceptual and application questions where the notes support it."
    prompt = f"""You are SlowStudy, a careful educational assistant.
Learner level: {level}
Task: {task}
Use the supplied notes as the primary source. Do not invent facts or imply that details came from the notes if they did not.
For any inferred or outside knowledge, label it clearly. If the notes do not support a reliable answer, say so.
Check that answers directly match their questions and preserve technical terminology.
NOTES/TOPIC:
{notes[:16000]}"""
    with st.spinner("Building your study set…"):
        try:
            st.session_state["study_result"] = generate(prompt, temperature=0.15)
            st.session_state["study_result_kind"] = kind
        except (RuntimeError, ValueError) as exc:
            st.error(str(exc))

result = st.session_state.get("study_result", "")
if result:
    st.markdown("## Your study set")
    with st.container(border=True):
        st.markdown(result)
    st.download_button("Download study set", result, file_name="slowstudy-material.md", mime="text/markdown")
    if st.button("Clear study set"):
        st.session_state.pop("study_result", None)
        st.session_state.pop("study_result_kind", None)
        st.rerun()

with st.expander("Model status & study-quality note"):
    status = health_check()
    if status["ok"] and status["model_available"]:
        st.success(f"Model available: {status['configured_model']}")
    elif status["ok"]:
        st.warning(f"Ollama is reachable, but '{status['configured_model']}' was not listed as installed.")
    else:
        st.warning("Ollama is not reachable yet. Start Ollama to generate study materials.")
    st.caption("AI-generated explanations can be wrong. Verify formulas, derivations, and answers against your course materials.")
footer()

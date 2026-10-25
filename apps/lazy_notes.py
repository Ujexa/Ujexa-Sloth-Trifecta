import streamlit as st
from toolkit.local_ai import generate, health_check
from toolkit.ui import configure_page, footer

configure_page(
    "LazyNotes", "✳",
    "Turn a brain dump, meeting notes, or lecture notes into a clear summary and practical next steps.",
)

with st.container(border=True):
    st.markdown('<div class="section-label">01 / Your input</div>', unsafe_allow_html=True)
    notes = st.text_area(
        "Notes", height=260,
        placeholder="Paste your notes here…\n\nExample: We meet Friday at 2 PM. Ama prepares questions. Kofi shares notes Thursday.",
        label_visibility="collapsed",
        key="lazy_notes_input",
    )
    left, right = st.columns([2, 1])
    with left:
        style = st.selectbox("Writing style", ["Concise", "Detailed", "Student-friendly"], key="lazy_notes_style")
    with right:
        st.caption(f"{len(notes):,} characters · max 16,000")
    submitted = st.button("Organize notes", type="primary", disabled=not notes.strip(), use_container_width=True)

if submitted:
    prompt = f"""You are LazyNotes, a careful note-organizing assistant.
Style: {style}
Use only information present in the notes. Do not invent names, dates, commitments, or conclusions.
Preserve uncertainty. If a relative date such as 'Thursday' appears without a calendar date, keep it relative; do not guess a date.
Return these sections in Markdown:
## Summary
## Action items
## Dates or deadlines mentioned
## Open questions
If a section has no information, say 'Not specified in the notes.'
NOTES:
{notes[:16000]}"""
    with st.spinner("Organizing with your configured model…"):
        try:
            st.session_state["lazy_notes_result"] = generate(prompt)
        except (RuntimeError, ValueError) as exc:
            st.error(str(exc))

result = st.session_state.get("lazy_notes_result", "")
if result:
    st.markdown("## Your organized notes")
    with st.container(border=True):
        st.markdown(result)
    st.download_button("Download Markdown", result, file_name="lazynotes-summary.md", mime="text/markdown")
    if st.button("Clear result"):
        st.session_state.pop("lazy_notes_result", None)
        st.rerun()

with st.expander("Privacy & model status"):
    status = health_check()
    if status["ok"]:
        st.success(f"Ollama is reachable at {status['host']}.")
        if status["model_available"]:
            st.caption(f"Configured model: {status['configured_model']}")
        else:
            st.warning(f"Configured model '{status['configured_model']}' was not found. Check `ollama list`.")
    else:
        st.warning(f"Ollama is currently unreachable at {status['host']}. Start Ollama to use AI features.")
    st.markdown('<div class="privacy-note">Your notes are sent to the Ollama endpoint configured on this machine. For local-only processing, keep OLLAMA_HOST on localhost and do not enter highly sensitive data into untrusted remote endpoints.</div>', unsafe_allow_html=True)
footer()

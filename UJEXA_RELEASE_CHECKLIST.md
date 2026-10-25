# Ujexa release checklist

## Code and quality
- [x] Shared visual system applied to all three Streamlit frontends
- [x] Shared, deterministic filename classifier with sensitive-name guard
- [x] AI is optional for SlothSort and only receives unknown non-sensitive filenames
- [x] Downloadable Markdown output from LazyNotes and SlowStudy
- [x] CSV export and category filtering in SlothSort
- [x] Offline unit tests for classifier and local Ollama client
- [x] GitHub Actions workflow for compile and test checks
- [ ] Run the apps on the target Windows laptop and inspect responsive layout
- [ ] Test actual Gemma outputs on representative notes and study sheets
- [ ] Confirm no personal exports, secrets, or `.env` files are staged

## Deployment decision
- These are Python/Streamlit applications, not static frontend sites.
- A frontend-only Vercel deployment will not execute the Streamlit Python apps or provide Ollama.
- Public deployment requires compatible Python hosting plus a secured model endpoint.
- SlothSort folder paths refer to the Streamlit host filesystem. Keep it local until a browser-upload or desktop-safe workflow is implemented for public use.
- Do not publish an unauthenticated Ollama endpoint. Avoid public model hosting for private user notes unless the privacy implications are explicit.

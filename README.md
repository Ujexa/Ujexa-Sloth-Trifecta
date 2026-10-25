# Slow & Steady AI Toolkit

**Three local-first tools to remove repetitive work:** SlothSort, LazyNotes, and SlowStudy.

| App | What it does | AI use |
| --- | --- | --- |
| **SlothSort** | Categorizes filenames, flags sensitive-looking names, exports a CSV report | Optional Ollama fallback for unknown, non-sensitive file types |
| **LazyNotes** | Summarizes notes into action items, deadlines, and open questions | Ollama text generation |
| **SlowStudy** | Generates revision summaries, flashcards, and practice questions | Ollama text generation |

## Status

The shared interface includes a user-controlled light/dark theme, responsive layout rules, consistent spacing and typography, accessible focus-friendly controls, and reduced-motion handling. This is an actively developed prototype. UI and deterministic classification tests are included. AI output quality is not guaranteed; review results before relying on them.

## Requirements

- Python 3.10 or later
- [Ollama](https://ollama.com/download) for AI features
- A model installed in Ollama, such as `gemma3:1b` (model choice depends on system resources)

The Streamlit interfaces and SlothSort's extension-based categorization work without an AI model. AI actions require a running Ollama service. Downloading software and model weights initially requires internet; inference can then run locally.

## Run on Windows

Open PowerShell in the repository root:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
ollama pull gemma3:1b
```

Launch each application in its own terminal:

```powershell
.\\.venv\\Scripts\\python.exe -m streamlit run apps/lazy_notes.py --server.port 8501
.\\.venv\\Scripts\\python.exe -m streamlit run apps/slow_study.py --server.port 8502
.\\.venv\\Scripts\\python.exe -m streamlit run apps/sloth_sort.py --server.port 8503
```

Open `http://localhost:8501`, `http://localhost:8502`, or `http://localhost:8503`.

## Run on macOS/Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
ollama pull gemma3:1b
.venv/bin/python -m streamlit run apps/lazy_notes.py
```

Use the equivalent command for `slow_study.py` or `sloth_sort.py` to run the other apps.

## Configuration

The apps read these environment variables:

- `OLLAMA_HOST` — defaults to `http://localhost:11434`
- `OLLAMA_MODEL` — defaults to `gemma3:1b`

Keep `OLLAMA_HOST` pointed to localhost for local-only processing. If you set it to another machine, the text sent to the model will leave your computer and you must trust and secure that endpoint.

## Privacy and safety

- **LazyNotes and SlowStudy:** submitted text is sent to the configured Ollama endpoint. Run Ollama locally if you want to keep text on your machine.
- **SlothSort:** scans filenames in the selected folder, not file contents. It never moves, renames, or deletes files.
- Filenames that look like passwords, recovery codes, private keys, or credentials are flagged before the optional AI step and excluded from its prompt.
- Filename extensions are heuristics, not proof of a file's contents. Unknown types remain marked for review.
- AI-generated output may be incorrect or incomplete. Verify dates, study answers, and categories.
- Do not commit `.env`, personal files, secrets, or recovery codes to Git.

## Testing

```bash
python -m pytest -q
```

The tests cover the shared Ollama client and deterministic SlothSort classification rules. They do not require downloading or running a model.

## Deployment notes

These apps use Streamlit and an Ollama model endpoint. A frontend-only deployment to Vercel will **not** automatically provide Python/Streamlit execution or a local Ollama model. For a public deployment, host the Streamlit app on a compatible Python service and configure an accessible, secured Ollama service; never expose an unauthenticated Ollama endpoint to the public internet. Public hosting changes the privacy model, so make that explicit to users. **Important for SlothSort:** a path entered into the app is a path on the machine running Streamlit, not a visitor’s laptop. Keep SlothSort local for folder scanning, or add an explicit browser file-upload workflow before publishing it as a public web utility.

For local demos and a first release, the recommended path is to publish this repository and run the three apps locally. Do not claim a public hosted demo is available until a compatible host and model endpoint have been configured and tested.

## Project structure

```text
slow-and-steady-ai-toolkit/
  apps/                 # Three Streamlit frontends
  toolkit/              # Shared design system, classifier, local AI client
  tests/                # Offline tests
  .streamlit/config.toml
  .env.example
  .gitignore
  LICENSE
  README.md
  requirements.txt
```

## Why open innovation matters

The applications use a replaceable Ollama endpoint rather than a proprietary hosted AI API. Users can inspect and modify the code, choose a supported model, and use local inference without sending text to a third-party model provider. Software and model downloads require initial internet access; after they are installed, local inference can work offline as long as the Ollama service and model remain available.

## License

MIT. See [LICENSE](LICENSE).

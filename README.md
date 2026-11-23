# StudyMate

StudyMate is a Streamlit chatbot that helps students plan study time, calculate
days until an exam, and divide study hours among subjects using Gemini and
LangChain tools.

## Setup

```powershell
cd "F:\study planner"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run

```powershell
.\run_app.bat
```

Enter a Gemini API key in the sidebar. The key is not stored by the app.
The default model is `gemini-3.6-flash`; it can be changed with the
`GEMINI_MODEL` environment variable.

## Test

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

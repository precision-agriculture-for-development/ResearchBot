# ResearchBot

This is a StreamLit app fronting the Assistant API or Vector Stores & Respones API for the experiment registry

Ensure `uv` is installed.

Clone the repo and `cd ResearchBot`:

Create a virtual environment 

`uv venv`

Activate it.

`.\venv\Scripts\activate`

Add the relevant libraries:

`uv add openai streamlit`

Put your OpenAI API key, Assistant ID and Vector Store ID into `.streamlit\secrets.toml`

- `OPENAI_API_KEY="xxxxxxx"`
- `ASSISTANT_ID="aaaaa"`
- `VECTOR_STORE_ID="dsfsdfds"`


Run the app:

`streamlit run main.py`


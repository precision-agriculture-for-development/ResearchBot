# ResearchBot

This is a StreamLit app fronting the Assistant API for the experiment registry

Ensure `uv` is installed.

Clone the repo and `cd ResearchBot`:

Create a virtual environment 

`uv venv`

Activate it.

`.\venv\Scripts\activate`

Add the relevant libraries:

`uv add openai streamlit`

Put your OpenAI API key and Assistant ID into `.streamlit\secrets.toml`

- `OPENAI_API_KEY=xxxxxxx`
- `ASSISTANT_ID=aaaaa`


Run the app:

`streamlit run main.py`


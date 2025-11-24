# Health-Care-Chatbot

## Overview
- Chatbot that answers health-related queries using intents and pattern matching, with optional neural model.
- Ownership: MIT License © 2025 Hemanth.

## Setup
- Install Python packages:
  - `python -m pip install numpy nltk`
  - Optional (for neural model): `python -m pip install tensorflow==2.15.*`
  - Optional (for web UI): `python -m pip install flask`
- Download NLTK data (optional but recommended):
  - `python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('wordnet')"`

## Train
- Lightweight Naive Bayes (no TensorFlow required):
  - `python training_py.py`
  - Produces `nb_model.pkl`, `words.pkl`, `classes.pkl`
- Neural model (TensorFlow):
  - Ensure TensorFlow is installed for your Python/OS
  - `python training_py.py`
  - Produces `chatbotmodel.h5`, `words.pkl`, `classes.pkl`

## Run Locally
- CLI single inference:
  - `python -c "from chatbot_py import respond; print(respond('i got common cold'))"`
- CLI interactive:
  - `python chatbot_py.py`
- GUI (Tkinter):
  - `python gui.py`
- Web (browser):
  - Install Flask: `python -m pip install flask`
  - Start server: `python server.py`
  - Open: `http://localhost:8000/`

## Global Hosting (Browser)
- Any Python-friendly host will work. Typical options:
  - Render (Free): create a new Web Service, set `Start Command` to `python server.py`, and add a disk for model files.
  - Railway / Fly.io: deploy with `python server.py` as the start command.
  - PythonAnywhere: create a Flask web app and point to `server.py`.
- Ensure these files are deployed: `server.py`, `chatbot_py.py`, `intents.json`, and either `nb_model.pkl` or `chatbotmodel.h5` plus `words.pkl`, `classes.pkl`.

## Model Selection Logic
- At runtime the chatbot loads in this order:
  - `chatbotmodel.h5` (Keras), else
  - `nb_model.pkl` (Naive Bayes), else
  - Fallback keyword matcher using `intents.json` patterns.

## Ownership
- License updated to `MIT License © 2025 Hemanth` in `LICENSE`.

<img src="https://www.scnsoft.com/blog-pictures/healthcare/how-chatbots-and-ai-are-changing-the-healthcare-industry_1.png">

    This chatbot will provide quick answers to FAQs by setting up rule-based keyword chatbots 
    with ¨if/then¨ logic. This chatbot will use a series of well-defined rules  to guide 
    customers through a series of menu options that can help answer their questions. 
    It will be there for customers 24/7 on their preferred channels, and simultaneously 
    handle more queries at once. 



<img src="https://miro.medium.com/max/875/1*69vLXZCjrJwdXytj0CTSiQ.jpeg">

PS: Please do not forget to drop a star if you like it!

<<<<<<< HEAD
# Translator System

A Streamlit web application for translating text between multiple languages. It uses `deep-translator` with Google Translate and displays any local translation history available in the project data directory.

## Run locally

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Deploy the live app

This is a Python/Streamlit server application, so it cannot be deployed to GitHub Pages. Use GitHub to store the source code, then deploy it from the repository with [Streamlit Community Cloud](https://share.streamlit.io/):

1. Push this project to a GitHub repository.
2. Open Streamlit Community Cloud and select **Create app**.
3. Authorize GitHub and choose the repository and its `main` branch.
4. Set the main file path to `app.py`, then deploy.

The app will receive a URL in the form `https://<your-app-name>.streamlit.app`.

## Deployment notes

- `requirements.txt` contains the tested Python dependencies.
- `data/translation_history.csv` is intentionally ignored by Git because it can contain user-entered text. Any runtime file storage on Streamlit Community Cloud is not durable; use a hosted database or object storage if persistent shared history is required.
- No app secrets are currently required. Google Translate requests are made through the `deep-translator` package, so translation availability is subject to that upstream service.
=======
# Translator_System
Multi-language text translator built with Streamlit and Google Translate, with local history tracking.
>>>>>>> 7e5e1afcee3d3776a383d9f83b76a2050f13533b

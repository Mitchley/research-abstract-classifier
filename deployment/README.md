# Deployment — Research Abstract Classifier

## Run Locally
```bash
cd deployment
pip install -r requirements.txt
streamlit run app.py
```
Opens at http://localhost:8501

## Files
- `app.py` — Streamlit web interface
- `best_model.joblib` — trained classifier (from Q2)
- `vectorizer.joblib` — TF-IDF vectorizer (from Q2)
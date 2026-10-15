# Research Abstract Classifier

A data science project built for SANalytics that classifies research abstracts into AI and Classical categories, summarizes a research corpus, discovers latent topics with LDA, and deploys the best classifier as a Streamlit app.

**Live app:** https://p5wiapqtaoavdmv9q4gacu.streamlit.app/

Source: MATANGA NY (2026).

---

## Structure

- `data/` — original dataset, cleaned dataset, and five-article corpus
- `notebooks/` — Q1 through Q4 notebooks
- `deployment/` — Streamlit app and serialized model
- `outputs/` — plots and the interactive pyLDAvis map

---

## Notebooks

**Q1 Baseline Model** (`Q1_baseline_model.ipynb`)
Preprocessing, TF-IDF features, Logistic Regression with balanced class weights. Test accuracy 88.60%, macro F1 0.8285.

**Q2 Improved Models and Deployment** (`Q2_models.ipynb`)
Linear SVM, Random Forest, XGBoost, and Naive Bayes compared. GridSearchCV enhancement applied to the winning model (Linear SVM). Tuned model saved for deployment. Macro F1 0.8771.

**Q3 Corpus Summarization** (`Q3_summarization.ipynb`)
Five research articles denoised with spaCy. TextRank extractive summary for the first article; LSA extractive summary for the remaining four, with word cloud visualizations.

**Q4 Topic Modeling** (`Q4_topic_modeling.ipynb`)
LDA with three topics on the corpus. Top words per topic, document-topic heatmap, and an interactive pyLDAvis Intertopic Distance Map.

---

## Deployment

**Live app:** https://p5wiapqtaoavdmv9q4gacu.streamlit.app/

The classifier is deployed publicly as a Streamlit app. Users can paste any abstract to receive a prediction with confidence scores, or load random AI or Classical samples to compare against known labels.

Deployment instructions are in `deployment/README.md`.

---

## Local Setup

Clone the repository, install `requirements.txt`, download the NLTK and spaCy resources, then run:

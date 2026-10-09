import streamlit as st
import joblib
import json
import re
import random
from pathlib import Path
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

st.set_page_config(page_title="Research Abstract Classifier", layout="wide")
st.title("Research Abstract Classifier")
st.markdown("Paste a research abstract to classify it as **AI** or **Classical**.")

# --- Base directory for reliable file paths ---
BASE_DIR = Path(__file__).resolve().parent

# --- Load model + vectorizer ---
try:
    model = joblib.load(BASE_DIR / "best_model.joblib")
    vectorizer = joblib.load(BASE_DIR / "vectorizer.joblib")
except FileNotFoundError:
    st.error("Model files not found. Train in Q2 first.")
    st.stop()

# --- Load dataset for the "load sample" convenience button ---
@st.cache_data
def load_samples():
    with open(BASE_DIR / "../data/research_abstracts_clean.json", encoding="utf-8") as f:
        return json.load(f)

samples = load_samples()

# --- Denoising pipeline (must match Q1) ---
STOP = set(stopwords.words('english')) | {
    'paper','study','result','research','using','used','based',
    'propose','proposed','method','model','show','however','thus','also'
}
LEM = WordNetLemmatizer()

def clean(text):
    text = re.sub(r'\[Formula:\s*see\s*text\]', ' ', str(text), flags=re.I)
    text = re.sub(r'\\u[0-9a-fA-F]{4}', ' ', text)
    text = re.sub(r'<[^>]+>|http\S+|10\.\d{4,9}/\S+', ' ', text)
    text = text.encode('ascii', 'ignore').decode('ascii').lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    return ' '.join(LEM.lemmatize(w) for w in text.split()
                    if w not in STOP and len(w) > 2)

# --- Session state for sample loading ---
if "text_input" not in st.session_state:
    st.session_state.text_input = ""
if "true_label" not in st.session_state:
    st.session_state.true_label = None

# --- Sidebar ---
with st.sidebar:
    st.header("Options")
    if st.button("Load random sample from dataset"):
        idx = random.randint(0, len(samples) - 1)
        s = samples[idx]
        st.session_state.text_input = s["abstract"]
        st.session_state.true_label = s["label"]
    if st.button("Clear"):
        st.session_state.text_input = ""
        st.session_state.true_label = None

# --- Text area (bound to session state) ---
text = st.text_area("Abstract:", value=st.session_state.text_input, height=250)
st.session_state.text_input = text

# --- Show ground-truth label if the sample came from the dataset ---
if st.session_state.true_label:
    st.caption(f"Ground-truth label of the loaded sample: **{st.session_state.true_label.upper()}**")

# --- Predict ---
if st.button("Predict"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        cleaned = clean(text)
        X = vectorizer.transform([cleaned])
        pred = model.predict(X)[0]
        prob = model.predict_proba(X)[0]
        ai_idx = list(model.classes_).index("ai")
        p_ai = prob[ai_idx]
        p_cl = 1 - p_ai

        st.success(f"**Prediction:** {pred.upper()}")
        st.write(f"Confidence - AI: {p_ai:.3f} | Classical: {p_cl:.3f}")

        if st.session_state.true_label:
            if pred == st.session_state.true_label:
                st.markdown("**Correct** - model agrees with the dataset label.")
            else:
                st.markdown(f"**Incorrect** - dataset says `{st.session_state.true_label}`, model said `{pred}`.")import streamlit as st
import joblib
import json
import re
import random
from pathlib import Path
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

st.set_page_config(page_title="Research Abstract Classifier", layout="wide")
st.title("Research Abstract Classifier")
st.markdown("Paste a research abstract to classify it as **AI** or **Classical**.")

# --- Base directory for reliable file paths ---
BASE_DIR = Path(__file__).resolve().parent

# --- Load model + vectorizer ---
try:
    model = joblib.load(BASE_DIR / "best_model.joblib")
    vectorizer = joblib.load(BASE_DIR / "vectorizer.joblib")
except FileNotFoundError:
    st.error("Model files not found. Train in Q2 first.")
    st.stop()

# --- Load dataset for the "load sample" convenience button ---
@st.cache_data
def load_samples():
    with open(BASE_DIR / "../data/research_abstracts_clean.json", encoding="utf-8") as f:
        return json.load(f)

samples = load_samples()

# --- Denoising pipeline (must match Q1) ---
STOP = set(stopwords.words('english')) | {
    'paper','study','result','research','using','used','based',
    'propose','proposed','method','model','show','however','thus','also'
}
LEM = WordNetLemmatizer()

def clean(text):
    text = re.sub(r'\[Formula:\s*see\s*text\]', ' ', str(text), flags=re.I)
    text = re.sub(r'\\u[0-9a-fA-F]{4}', ' ', text)
    text = re.sub(r'<[^>]+>|http\S+|10\.\d{4,9}/\S+', ' ', text)
    text = text.encode('ascii', 'ignore').decode('ascii').lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    return ' '.join(LEM.lemmatize(w) for w in text.split()
                    if w not in STOP and len(w) > 2)

# --- Session state for sample loading ---
if "text_input" not in st.session_state:
    st.session_state.text_input = ""
if "true_label" not in st.session_state:
    st.session_state.true_label = None

# --- Sidebar ---
with st.sidebar:
    st.header("Options")
    if st.button("Load random sample from dataset"):
        idx = random.randint(0, len(samples) - 1)
        s = samples[idx]
        st.session_state.text_input = s["abstract"]
        st.session_state.true_label = s["label"]
    if st.button("Clear"):
        st.session_state.text_input = ""
        st.session_state.true_label = None

# --- Text area (bound to session state) ---
text = st.text_area("Abstract:", value=st.session_state.text_input, height=250)
st.session_state.text_input = text

# --- Show ground-truth label if the sample came from the dataset ---
if st.session_state.true_label:
    st.caption(f"Ground-truth label of the loaded sample: **{st.session_state.true_label.upper()}**")

# --- Predict ---
if st.button("Predict"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        cleaned = clean(text)
        X = vectorizer.transform([cleaned])
        pred = model.predict(X)[0]
        prob = model.predict_proba(X)[0]
        ai_idx = list(model.classes_).index("ai")
        p_ai = prob[ai_idx]
        p_cl = 1 - p_ai

        st.success(f"**Prediction:** {pred.upper()}")
        st.write(f"Confidence - AI: {p_ai:.3f} | Classical: {p_cl:.3f}")

        if st.session_state.true_label:
            if pred == st.session_state.true_label:
                st.markdown("**Correct** - model agrees with the dataset label.")
            else:
                st.markdown(f"**Incorrect** - dataset says `{st.session_state.true_label}`, model said `{pred}`.")import streamlit as st
import joblib
import json
import re
import random
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

st.set_page_config(page_title="Research Abstract Classifier", layout="wide")
st.title("Research Abstract Classifier")
st.markdown("Paste a research abstract to classify it as **AI** or **Classical**.")

# --- Load model + vectorizer ---
try:
    model = joblib.load(BASE_DIR / "best_model.joblib")
    vectorizer = joblib.load(BASE_DIR / "vectorizer.joblib")
except FileNotFoundError:
    st.error("Model files not found. Train in Q2 first.")
    st.stop()

# --- Load dataset for the "load sample" convenience button ---
@st.cache_data
def load_samples():
    with open("../data/research_abstracts_clean.json", encoding="utf-8") as f:
        return json.load(f)

samples = load_samples()

# --- Denoising pipeline (must match Q1) ---
STOP = set(stopwords.words('english')) | {
    'paper','study','result','research','using','used','based',
    'propose','proposed','method','model','show','however','thus','also'
}
LEM = WordNetLemmatizer()

def clean(text):
    text = re.sub(r'\[Formula:\s*see\s*text\]', ' ', str(text), flags=re.I)
    text = re.sub(r'\\u[0-9a-fA-F]{4}', ' ', text)
    text = re.sub(r'<[^>]+>|http\S+|10\.\d{4,9}/\S+', ' ', text)
    text = text.encode('ascii', 'ignore').decode('ascii').lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    return ' '.join(LEM.lemmatize(w) for w in text.split()
                    if w not in STOP and len(w) > 2)

# --- Session state for sample loading ---
if "text_input" not in st.session_state:
    st.session_state.text_input = ""
if "true_label" not in st.session_state:
    st.session_state.true_label = None

# --- Sidebar ---
with st.sidebar:
    st.header("Options")
    if st.button("Load random sample from dataset"):
        idx = random.randint(0, len(samples) - 1)
        s = samples[idx]
        st.session_state.text_input = s["abstract"]
        st.session_state.true_label = s["label"]
    if st.button("Clear"):
        st.session_state.text_input = ""
        st.session_state.true_label = None

# --- Text area (bound to session state) ---
text = st.text_area("Abstract:", value=st.session_state.text_input, height=250)
st.session_state.text_input = text

# --- Show ground-truth label if the sample came from the dataset ---
if st.session_state.true_label:
    st.caption(f"Ground-truth label of the loaded sample: **{st.session_state.true_label.upper()}**")

# --- Predict ---
if st.button("Predict"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        cleaned = clean(text)
        X = vectorizer.transform([cleaned])
        pred = model.predict(X)[0]
        prob = model.predict_proba(X)[0]
        ai_idx = list(model.classes_).index("ai")
        p_ai = prob[ai_idx]
        p_cl = 1 - p_ai

        st.success(f"**Prediction:** {pred.upper()}")
        st.write(f"Confidence - AI: {p_ai:.3f} | Classical: {p_cl:.3f}")

        if st.session_state.true_label:
            if pred == st.session_state.true_label:
                st.markdown("**Correct** - model agrees with the dataset label.")
            else:
                                st.markdown(f"**Incorrect** - dataset says `{st.session_state.true_label}`, model said `{pred}`.")

# PhishGuard: Email Threat Detection System

PhishGuard is a machine learning-powered email threat detection application designed to classify emails into three categories in real-time:
- **🟢 HAM (Legitimate)**
- **🟠 SPAM (Unsolicited)**
- **🔴 PHISHING (Threat)**

It combines a trained **Ensemble Voting Classifier** with a **Heuristic Rule-Based Layer** to provide highly accurate predictions, particularly for borderline cases. The application features a sleek, dark-mode web interface built with **Streamlit**.

## 🚀 Overview

The system uses a two-step detection mechanism:
1. **Machine Learning Model:** Text is preprocessed (HTML tags removed, URLs tokenized) and transformed using a Vectorizer (TF-IDF). An Ensemble Voting Classifier (built using `scikit-learn`) then computes the probability of the email belonging to each class.
2. **Heuristic Layer:** A rule-based scoring system scans for common spam signals (e.g., "free iphone", "act now") and phishing signals (e.g., "verify your account", "secure link"). If the heuristic score crosses a certain threshold, or if the ML model is uncertain but heuristics strongly suggest a threat, the prediction is upgraded to Spam or Phishing.

## 📂 Dataset Sources
The model was trained on a diverse and comprehensive set of publicly available email corpora located in the `datasets/` directory:
- **Enron Corpus** (`Enron.csv`): A massive collection of real-world corporate emails, primarily used as the baseline for Legitimate (Ham) emails.
- **Nazario Phishing Corpus** (`Nazario.csv`): A specialized dataset containing verified, real-world phishing emails.
- **SpamAssassin Public Corpus** (`SpamAssasin.csv`): A well-known mix of standard spam and ham emails.
- **CEAS 2008 Challenge** (`CEAS_08.csv`): Additional diverse email data to improve the model's robustness against complex spam and phishing campaigns.

These datasets were merged, cleaned, and heavily preprocessed in `Notebook/spam_phishing_detector.ipynb` to create a robust, multi-class training dataset.

## 📈 Model & Results

The complete data exploration, preprocessing, model training, and evaluation pipeline is detailed in `Notebook/spam_phishing_detector.ipynb`.

- **Model Architecture:** The core ML engine is an **Ensemble Voting Classifier** that aggregates the predictions of multiple underlying models to improve overall accuracy and generalization.
- **Feature Engineering:** Natural Language Processing (NLP) techniques, including lowercasing, regex cleaning, URL tokenization, and vectorization.
- **Performance:** By combining datasets from different eras and domains, the model avoids overfitting to a specific type of spam and achieves high accuracy in distinguishing between benign marketing (spam) and malicious intent (phishing). The heuristic rules implemented in `app.py` further eliminate false negatives on zero-day phishing patterns.

## 🛠️ Tech Stack
- **Python 3**
- **scikit-learn** (Machine Learning & NLP pipelines)
- **pandas & numpy** (Data manipulation)
- **Streamlit** (Frontend Web Interface)

## 🏃‍♂️ How to Run Locally

1. **Clone the repository.**
2. **Install dependencies:** 
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```
4. Open your browser to the local URL provided (usually `http://localhost:8501`). You can paste email content into the text area to test the detection engine.
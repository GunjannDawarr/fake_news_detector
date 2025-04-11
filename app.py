import streamlit as st
import joblib
from newspaper import build, Article

# Load your trained vectorizer and model
vectorizer = joblib.load("vectorizer.jb")
model = joblib.load("lr_model.jb")

# ----------------------
# Scrape latest articles
# ----------------------
def scrape_articles():
    paper = build('https://www.ndtv.com', memoize_articles=False)
    articles = []

    for article in paper.articles[:5]:  # scrape first 5
        try:
            article.download()
            article.parse()
            title = article.title
            text = article.text
            combined = f"{title} {text}"
            articles.append((title, combined))
        except:
            continue

    return articles

# ----------------------
# Predict function
# ----------------------
def predict(text):
    cleaned_text = text.lower()
    vector = vectorizer.transform([cleaned_text])
    prediction = model.predict(vector)[0]
    return "Real" if prediction == 1 else "Fake"

# ----------------------
# Streamlit UI
# ----------------------
st.set_page_config(page_title="Fake News Detector", page_icon="🧠", layout="centered")
st.title("🧠 Real-Time Fake News Detector")

st.markdown("### 📰 Check live news articles")
if st.button("Fetch Real-Time News"):
    with st.spinner("Scraping live news..."):
        scraped_articles = scrape_articles()
        if scraped_articles:
            for i, (title, content) in enumerate(scraped_articles):
                label = predict(content)
                st.markdown(f"{i+1}. [{label}]** {title}")
                st.markdown("---")
        else:
            st.warning("Couldn't fetch any articles or website blocked scraping.")

# ------------------------------------
st.markdown("### ✍ Or enter your own news text")

user_input = st.text_area("Paste news headline or content here:")

if st.button("Check My News"):
    if user_input.strip():
        label = predict(user_input)
        st.success(f"The News is *{label}*!")
    else:
        st.warning("Please enter some news text first.")
        
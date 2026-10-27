---
num: 25
title: "NLP and Text Analytics: Cleaning, TF-IDF, Sentiment Classification, Topics and Embeddings"
live: "ML track (added) · GenAI bridge"
updated: "scikit-learn 1.7+ · 2026 practice"
level: Advanced
duration: 130 min
summary: Turn customer reviews into insight. Text cleaning and tokenisation, stop words, stemming and lemmatisation, bag-of-words and TF-IDF with n-grams, a sentiment classifier with error analysis, aspect-level insight, topic modelling with NMF, document similarity, and how embeddings and LLMs change NLP, on 3,000 e-commerce reviews.
datasets: [customer_reviews.csv]
outcomes:
  - Clean and tokenise text and decide when to remove stop words, stem or lemmatise
  - Represent documents with bag-of-words and TF-IDF (with n-grams) and read the vocabulary
  - Train, evaluate and interpret a sentiment classifier, including error analysis
  - Extract topics with NMF and aspect-level sentiment with simple rules
  - Explain word and sentence embeddings and when to use LLMs instead
---

## The NLP pipeline

```python fig: A classical text-analytics pipeline.
dg.flow(["Raw text", "Clean &\ntokenise", "Vectorise\n(BoW, TF-IDF,\nembeddings)", "Model\n(classify, cluster,\ntopics)", "Insight &\naction"], title="Text analytics pipeline")
```

```python run
import pandas as pd, numpy as np, re
pd.set_option("display.width", 160); pd.set_option("display.max_colwidth", 90)
rv = pd.read_csv("customer_reviews.csv", parse_dates=["date"])
print(rv.shape, rv.sentiment.value_counts(normalize=True).round(3).to_dict())
print(rv.groupby("product").rating.mean().round(2).sort_values().to_dict())
print(rv.sample(5, random_state=3)[["rating", "review_text"]].to_string(index=False))
rv["n_words"] = rv.review_text.str.split().str.len()
print("words per review:", rv.n_words.describe().round(1)[["mean", "50%", "max"]].to_dict(), "| by sentiment:", rv.groupby("sentiment").n_words.mean().round(1).to_dict())
```

## Cleaning and tokenising

```python run
STOP = {"the", "a", "an", "is", "it", "and", "to", "of", "for", "in", "on", "was", "this", "that", "with", "my", "i", "very", "so", "are", "be", "at", "as", "after", "all"}
NEGATIONS = {"not", "no", "never", "don't", "can't", "isn't", "wasn't"}
FIX = {"batery": "battery", "qualty": "quality", "delivry": "delivery", "realy": "really", "scren": "screen", "wroth": "worth", "bekaar": "useless", "badiya": "good"}
def clean(text, remove_stop=True):
    t = text.lower()
    t = re.sub(r"[:;]-?[()]", " ", t)                       # emoticons
    t = re.sub(r"[^a-z' ]+", " ", t)                        # keep letters and apostrophes
    tokens = [FIX.get(w, w) for w in t.split()]
    if remove_stop: tokens = [w for w in tokens if w not in STOP or w in NEGATIONS]
    return " ".join(tokens)
ex = rv.review_text.iloc[7]
print("raw:  ", ex); print("clean:", clean(ex))
rv["clean"] = rv.review_text.map(clean)
```

| Step | Purpose | Caution |
|---|---|---|
| Lower-casing | "Battery" = "battery" | Loses emphasis ("GREAT") |
| Remove punctuation, numbers, URLs | Reduce noise | Prices and model numbers may matter |
| Spelling / slang normalisation | Merge variants ("batery", Hinglish "badiya") | Needs a dictionary |
| Stop-word removal | Drop frequent function words | **Never** drop negations ("not") for sentiment |
| Stemming (Porter, Snowball) | "charging", "charged" → "charg" | Crude, can merge different words |
| Lemmatisation (spaCy) | "better" → "good", "batteries" → "battery" | Slower, needs a language model |

Libraries: **spaCy** (fast tokenisation, lemmas, entities), **NLTK** (classic teaching toolkit), **regex**; for Indian languages, **IndicNLP** and multilingual models.

## Bag-of-words and TF-IDF

**Bag-of-words** counts each word per document, ignoring order. **TF-IDF** down-weights words that appear in many documents (like "product") and up-weights distinctive ones:

$$\text{tfidf}(t, d) = \text{tf}(t, d) \times \log\frac{1 + N}{1 + \text{df}(t)} + 1$$

```python run
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
docs = ["battery drains fast", "battery lasts all day", "screen is not great", "great screen and great battery"]
cv = CountVectorizer(); bow = cv.fit_transform(docs)
print(pd.DataFrame(bow.toarray(), columns=cv.get_feature_names_out(), index=[f"doc{i}" for i in range(4)]))
tf = TfidfVectorizer(); tfm = tf.fit_transform(docs)
print(pd.DataFrame(tfm.toarray().round(2), columns=tf.get_feature_names_out(), index=[f"doc{i}" for i in range(4)]).loc[:, ["battery", "great", "not", "drains"]])
bi = CountVectorizer(ngram_range=(1, 2)).fit(["screen is not great"]); print("with bigrams:", bi.get_feature_names_out().tolist())
```

Bigrams such as "not great" keep some word order, which matters for sentiment.

## Sentiment classifier

```python run
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
Xtr, Xte, ytr, yte = train_test_split(rv.clean, rv.sentiment, test_size=0.25, stratify=rv.sentiment, random_state=0)
for name, vec in [("unigrams", TfidfVectorizer(min_df=2)), ("uni + bigrams", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True))]:
    m = make_pipeline(vec, LogisticRegression(max_iter=3000, C=5)).fit(Xtr, ytr)
    print(f"{name:14s} accuracy {accuracy_score(yte, m.predict(Xte)):.3f} | vocabulary {len(m[0].vocabulary_):,}")
clf = m
print(classification_report(yte, clf.predict(Xte), digits=3))
labels = ["negative", "neutral", "positive"]
print(pd.DataFrame(confusion_matrix(yte, clf.predict(Xte), labels=labels), index=[f"true {l}" for l in labels], columns=[f"pred {l}" for l in labels]))
```

### What did it learn?

```python run
vocab = np.array(clf[0].get_feature_names_out())
for i, c in enumerate(clf[-1].classes_):
    top = np.argsort(-clf[-1].coef_[i])[:8]; print(f"{c:9s} ←", vocab[top].tolist())
```

### Error analysis

```python run
pred = clf.predict(Xte); proba = clf.predict_proba(Xte).max(1)
err = pd.DataFrame({"text": rv.loc[Xte.index, "review_text"], "rating": rv.loc[Xte.index, "rating"], "true": yte, "pred": pred, "confidence": proba.round(2)})[pred != yte]
print(len(err), "errors"); print(err.sort_values("confidence", ascending=False).head(6).to_string(index=False))
```

Reading errors is the most useful step in NLP. Typical causes here: **noisy labels** (a 1-star rating on a positive text), **mixed** reviews ("good screen but weak battery") and genuinely neutral wording. Fixes include better labels, aspect-level models, or an LLM for difficult cases.

## Aspect-level insight

Overall sentiment hides *what* customers like or dislike. A simple keyword approach already gives actionable results:

```python run
ASPECTS = {"battery": r"batter|charg", "screen": r"screen|display|pixel|touch", "sound": r"sound|bass|speaker|mic", "build": r"build|hinge|button|finish|plastic",
           "delivery": r"deliver|courier|box|packag|arriv", "service": r"support|service|refund|replacement|care", "price": r"price|money|rupee|expensive|worth", "software": r"app|update|bloatware|setup"}
low = rv.review_text.str.lower()
rows = []
for a, pat in ASPECTS.items():
    m = low.str.contains(pat, regex=True)
    rows.append({"aspect": a, "mentions": int(m.sum()), "share_negative_%": round(100 * (rv.sentiment[m] == "negative").mean(), 1), "avg_rating": round(rv.rating[m].mean(), 2)})
asp = pd.DataFrame(rows).sort_values("share_negative_%", ascending=False); print(asp.to_string(index=False))
print(rv.assign(battery=low.str.contains(ASPECTS["battery"])).query("battery").groupby("product").rating.mean().round(2).sort_values().head(3).to_dict())
```

Production systems use **aspect-based sentiment analysis** models or LLM prompts ("list each product aspect mentioned and its sentiment as JSON").

## Topic modelling

**Topic models** discover groups of words that co-occur, without labels. **NMF** on TF-IDF is fast and gives readable topics (LDA on counts is the classic alternative; BERTopic uses embeddings).

```python run
from sklearn.decomposition import NMF
tfidf = TfidfVectorizer(max_df=0.5, min_df=5, ngram_range=(1, 2), stop_words="english")
Xt = tfidf.fit_transform(rv.review_text.str.lower())
nmf = NMF(n_components=6, random_state=0, init="nndsvda", max_iter=500).fit(Xt)
terms = np.array(tfidf.get_feature_names_out())
for k, comp in enumerate(nmf.components_): print(f"topic {k}:", ", ".join(terms[np.argsort(-comp)[:7]]))
rv["topic"] = nmf.transform(Xt).argmax(1)
print(rv.groupby("topic").agg(reviews=("rating", "size"), avg_rating=("rating", "mean")).round(2).T)
```

Name each topic from its top words (for example "battery and charging", "delivery and packaging") and track topic volume and rating over time.

## Similarity search

```python run
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
lsa = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), min_df=2, stop_words="english"), TruncatedSVD(100, random_state=0)).fit(rv.review_text)
E = lsa.transform(rv.review_text)
for query in ["the battery runs out quickly and charging takes forever", "phone heats up and power does not last"]:
    sims = cosine_similarity(lsa.transform([query]), E)[0]; best = np.argsort(-sims)[:3]
    print("query:", query); [print(f"   {sims[i]:.2f}  {rv.review_text.iloc[i]}") for i in best]
```

Latent semantic analysis (TF-IDF + SVD) finds the charging complaints for the first query. The second query fails badly: "heats" and "power" never appear in the reviews and "last" is a different token from "lasts", so LSA matches the only shared word, "does". Word-count methods cannot know that "power does not last" means the battery drains. Modern **embeddings** do this far better.

## Embeddings and LLMs

| Approach | Idea | Use |
|---|---|---|
| Word2Vec, GloVe, fastText (2013–2016) | Each word gets a dense vector; similar words are close | Features, similarity |
| Transformers (BERT, 2018 →) | Contextual vectors: "bank" differs in "river bank" and "bank loan" | Fine-tuned classifiers, NER |
| Sentence embeddings (sentence-transformers, OpenAI/Cohere/Voyage/Gemini embedding APIs) | One vector per sentence or document | Semantic search, clustering, RAG |
| LLMs (Claude, GPT, Gemini, Llama) | Instruction-following generation | Zero-shot classification, extraction, summarisation |

```python
# Sentence embeddings (pip install sentence-transformers) – runs locally
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
emb = model.encode(rv.review_text.tolist(), normalize_embeddings=True)    # 3,000 × 384 matrix
# then: LogisticRegression on emb, KMeans on emb, or cosine search as above
```

```python
# Zero-shot classification with an LLM (see the GenAI track for API set-up and cost control)
prompt = """Classify the review's sentiment as positive, negative or neutral and list aspects mentioned.
Return JSON: {"sentiment": ..., "aspects": [{"aspect": ..., "sentiment": ...}]}
Review: "Good screen but the battery barely lasts half a day." """
```

**When to use what:** TF-IDF + logistic regression is cheap, fast, explainable and often within a few points of large models on simple tasks. Embeddings help with semantic similarity and small labelled sets. LLMs handle nuanced, multi-aspect or multilingual text with few or no labels, at higher cost and latency; validate them on a labelled sample just like any model.

## Summary

:::key
- Clean text deliberately: lower-case, normalise spelling and slang, keep negations; stem or lemmatise when useful.
- Bag-of-words counts words; TF-IDF weights distinctive words; bigrams capture short phrases like "not great".
- A TF-IDF + logistic regression classifier is a strong, explainable baseline; error analysis reveals noisy labels and mixed reviews.
- Aspect keywords and NMF topics turn reviews into product actions.
- Embeddings and LLMs capture meaning beyond exact words; benchmark them against the classical baseline.
:::

:::quiz
Q: Why should "not" be kept when removing stop words for sentiment?
* It flips meaning: "not good" vs "good"
- It is a long word
- TF-IDF needs it
- It is a noun
> Negations carry sentiment.

Q: What does IDF do in TF-IDF?
* Down-weights words that appear in many documents
- Counts words
- Removes stop words
- Translates words
> Common words get low weight.

Q: What do bigrams add?
* Pairs of consecutive words such as "not great", keeping some word order
- Two languages
- Two labels
- Double counts
> ngram_range=(1, 2).

Q: Which method finds topics without labels?
- Logistic regression
* NMF or LDA topic modelling
- Confusion matrix
- Stemming
> Unsupervised.

Q: What is a sentence embedding?
* A dense vector representing a sentence's meaning, so similar sentences are close
- A list of words
- A TF-IDF score
- A topic label
> Used for semantic search and RAG.

Q: When might TF-IDF + logistic regression be the better choice than an LLM?
* Simple, high-volume classification where cost, speed and explainability matter
- Never
- For multilingual sarcasm
- When there are no labels
> Always benchmark.
:::

:::exercise Practice
(1) Add a feature for exclamation marks and review length and test whether accuracy changes. (2) Track the monthly share of negative battery reviews. (3) Try `ComplementNB` and `LinearSVC` and compare macro F1. (4) Write an LLM prompt for aspect-based sentiment and test it on 10 reviews (GenAI track).
???
```python
from scipy.sparse import hstack
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import ComplementNB
from sklearn.metrics import f1_score
monthly = rv.assign(m=rv.date.dt.to_period("M"), batt=low.str.contains(ASPECTS["battery"])).query("batt").groupby("m").sentiment.apply(lambda s: (s == "negative").mean()); print(monthly.round(2))
for est in (ComplementNB(), LinearSVC(C=0.5)):
    mm = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), min_df=2), est).fit(Xtr, ytr); print(type(est).__name__, f1_score(yte, mm.predict(Xte), average="macro"))
```
:::

:::interview Questions you may be asked
**Q: How would you build a sentiment model for customer reviews?**
Define labels (stars or manual), clean text keeping negations, start with TF-IDF + logistic regression, evaluate with macro F1 and a confusion matrix, analyse errors, then try embeddings or a fine-tuned transformer/LLM if needed, and monitor drift.

**Q: TF-IDF vs embeddings?**
TF-IDF is sparse, exact-word based and interpretable; embeddings are dense and capture meaning, synonyms and context, at the cost of interpretability and compute.

**Q: How do you find what customers complain about most?**
Aspect extraction (keywords, NER, or LLM prompts) combined with sentiment per aspect, plus topic modelling to discover unexpected themes, tracked over time.
:::

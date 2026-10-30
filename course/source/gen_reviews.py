"""Generate customer_reviews.csv: 3,000 realistic e-commerce reviews for the NLP / text-classification lessons.

Unlike the small template set in product_reviews.csv, these reviews mix aspects, use negation ("not bad"),
contrast ("good screen but the battery is weak"), intensifiers, typos, Hinglish words and noisy star ratings,
so models score in a realistic range instead of 100%.
"""
import os
import numpy as np, pandas as pd

rng = np.random.default_rng(2026)
OUT = os.path.join(os.path.dirname(__file__), "..", "datasets", "customer_reviews.csv")

ASPECTS = {
    "battery": (["battery lasts all day", "battery backup is superb", "charges really fast", "battery easily lasts two days"],
                ["battery drains too fast", "battery barely lasts half a day", "charging is painfully slow", "battery swelled after a month"]),
    "screen": (["display is bright and sharp", "colours on the screen look vivid", "screen is crisp even outdoors"],
               ["screen is dull", "display has dead pixels", "screen scratches very easily", "touch is unresponsive at times"]),
    "sound": (["sound is clear and loud", "bass is rich", "calls are crystal clear"],
              ["sound is tinny", "speaker crackles at high volume", "mic quality is poor on calls"]),
    "build": (["build quality feels premium", "feels solid in the hand", "the finish is classy"],
              ["build feels cheap and plasticky", "buttons are loose", "the hinge broke within weeks"]),
    "delivery": (["delivery was quick", "arrived a day early", "packaging was neat and safe"],
                 ["delivery was late", "the box arrived damaged", "courier was rude and delayed it twice"]),
    "service": (["customer support solved my issue quickly", "replacement was smooth", "service centre staff were helpful"],
                ["customer care never replied", "refund is still pending after weeks", "service centre kept me waiting for days"]),
    "price": (["great value for money", "worth every rupee", "price is very reasonable for these features"],
              ["overpriced for what you get", "not worth the price", "too expensive compared to rivals"]),
    "software": (["the app is smooth", "updates arrive regularly", "setup took two minutes"],
                 ["the app keeps crashing", "too much bloatware", "updates made it slower"]),
}
NEUTRAL = ["it works as described", "average product for daily use", "nothing special, does the job", "okay for the price", "decent but could be better",
           "delivered on the expected date", "as expected", "it is fine", "mixed feelings so far", "will update after a month of use"]
INTENS = ["", "", "", "really ", "very ", "super ", "honestly ", "totally "]
OPEN_POS = ["", "", "Loved it! ", "Happy with the purchase. ", "Superb product. ", "Bahut badiya. ", "Highly recommend. "]
OPEN_NEG = ["", "", "Very disappointed. ", "Worst purchase ever. ", "Don't buy. ", "Bekaar product. ", "Regret buying this. "]
NEG_FLIP_POS = ["not bad at all", "can't complain", "no issues so far", "not disappointed"]          # negated negatives = positive
NEG_FLIP_NEG = ["not great", "not worth it", "not as good as advertised", "not happy with it"]     # negated positives = negative
TYPOS = {"battery": "batery", "quality": "qualty", "delivery": "delivry", "really": "realy", "excellent": "excelent", "screen": "scren", "worth": "wroth"}
PRODUCTS = ["Earbuds", "Smartphone", "Smartwatch", "Laptop", "Speaker", "Tablet"]


ADJ = {"fast", "bright", "sharp", "vivid", "clear", "loud", "rich", "solid", "premium", "classy", "quick", "early", "neat", "helpful", "smooth", "reasonable",
       "slow", "dull", "cheap", "poor", "late", "rude", "expensive", "tinny", "loose", "unresponsive", "superb", "easily", "painfully", "damaged"}


def phrase(aspect, good):
    words = rng.choice(ASPECTS[aspect][0 if good else 1]).split(" ")
    idx = [i for i, w in enumerate(words) if w in ADJ]
    if idx and rng.random() < .35:                                     # intensifier before an adjective: "very slow"
        i = int(rng.choice(idx)); words[i] = rng.choice(INTENS[3:]) + words[i]
    return " ".join(words)


def review(sent):
    aspects = list(rng.choice(list(ASPECTS), size=rng.integers(1, 4), replace=False))
    if sent == "neutral":
        parts = [rng.choice(NEUTRAL)]
        if rng.random() < .55:                                         # neutral = genuinely mixed
            a, b = rng.choice(list(ASPECTS), 2, replace=False)
            parts = [f"{phrase(a, True)} but {phrase(b, False)}"] + ([rng.choice(NEUTRAL)] if rng.random() < .5 else [])
        text = ". ".join(parts)
    else:
        good = sent == "positive"
        parts = [phrase(a, good) for a in aspects]
        if rng.random() < .3:                                          # contrast with a minor opposite point
            other = rng.choice([a for a in ASPECTS if a not in aspects])
            parts[-1] = parts[-1] + (" though the " if rng.random() < .5 else " but ") + phrase(other, not good).replace("the ", "", 1)
        if rng.random() < .25: parts.append(rng.choice(NEG_FLIP_POS if good else NEG_FLIP_NEG))
        text = (rng.choice(OPEN_POS if good else OPEN_NEG)) + ", ".join(parts)
    for k, v in TYPOS.items():
        if k in text and rng.random() < .08: text = text.replace(k, v, 1)
    text = ". ".join(s[:1].upper() + s[1:] for s in text.split(". "))          # capitalise each sentence
    if rng.random() < .3: text += rng.choice([".", "!", "!!", " :)", " :(" if sent == "negative" else "."])
    return text


rows = []
start = pd.Timestamp("2025-01-01")
for i in range(1, 3001):
    sent = rng.choice(["positive", "negative", "neutral"], p=[.52, .33, .15])
    rating = {"positive": rng.choice([4, 5], p=[.45, .55]), "negative": rng.choice([1, 2], p=[.6, .4]), "neutral": 3}[sent]
    if rng.random() < .07: rating = int(np.clip(rating + rng.choice([-2, -1, 1, 2]), 1, 5))    # noisy stars (people click the wrong star)
    label = "positive" if rating >= 4 else "negative" if rating <= 2 else "neutral"           # label derived from stars, like real datasets
    rows.append(dict(review_id=i, date=(start + pd.Timedelta(days=int(rng.integers(0, 365)))).date().isoformat(), product=rng.choice(PRODUCTS),
                     rating=rating, review_text=review(sent), sentiment=label, verified_purchase=bool(rng.random() < .85), helpful_votes=int(rng.poisson(2))))
df = pd.DataFrame(rows)
df.to_csv(OUT, index=False)
print(df.shape, df.sentiment.value_counts().to_dict(), df.review_text.nunique(), "unique texts")
print(df.sample(6, random_state=1)[["rating", "sentiment", "review_text"]].to_string(index=False))

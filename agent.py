import json
import math
import random
import re
from collections import Counter
from pathlib import Path

import config

# Pure-Python TF-IDF (no scikit-learn / numpy / pyarrow needed).
# Mirrors TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True).
STOP_WORDS = frozenset([
    "a", "about", "above", "across", "after", "afterwards", "again", "against", "all",
    "almost", "alone", "along", "already", "also", "although", "always", "am", "among",
    "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone",
    "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be",
    "became", "because", "become", "becomes", "becoming", "been", "before",
    "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond",
    "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due",
    "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty",
    "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere",
    "except", "few", "fifteen", "fifty", "fill", "find", "fire", "first", "five", "for",
    "former", "formerly", "forty", "found", "four", "from", "front", "full", "further",
    "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here",
    "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself",
    "his", "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile",
    "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much",
    "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless",
    "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now",
    "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other",
    "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part",
    "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since",
    "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something",
    "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten",
    "than", "that", "the", "their", "them", "themselves", "then", "thence", "there",
    "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they",
    "thick", "thin", "third", "this", "those", "though", "three", "through",
    "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very",
    "via", "was", "we", "well", "were", "what", "whatever", "when", "whence",
    "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon",
    "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole",
    "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you",
    "your", "yours", "yourself", "yourselves"
])

_TOKEN = re.compile(r"(?u)\b\w\w+\b")


def _features(text):
    """Lowercase, drop stop words, return unigrams + bigrams."""
    toks = [t for t in _TOKEN.findall(text.lower()) if t not in STOP_WORDS]
    return toks + [f"{a} {b}" for a, b in zip(toks, toks[1:])]


class _Tfidf:
    def __init__(self, docs):
        self.n = len(docs)
        counts = [Counter(_features(d)) for d in docs]
        df = Counter()
        for c in counts:
            df.update(c.keys())
        # smooth idf, same as scikit-learn's default
        self.idf = {t: math.log((1 + self.n) / (1 + f)) + 1.0 for t, f in df.items()}
        self.rows = [self._vec(c) for c in counts]
        # inverted index: term -> [(row, weight)] so a query only touches relevant rows
        self.index = {}
        for r, vec in enumerate(self.rows):
            for t, w in vec.items():
                self.index.setdefault(t, []).append((r, w))

    def _vec(self, counts):
        v = {t: (1.0 + math.log(c)) * self.idf[t] for t, c in counts.items() if t in self.idf}
        norm = math.sqrt(sum(w * w for w in v.values()))
        return {t: w / norm for t, w in v.items()} if norm else {}

    def scores(self, query):
        """Cosine similarity of the query against every row -> {row: score}."""
        q = self._vec(Counter(_features(query)))
        out = {}
        for t, qw in q.items():
            for r, w in self.index.get(t, ()):
                out[r] = out.get(r, 0.0) + qw * w
        return out


class FULAgent:
    """Intent-based retrieval over the FUL dataset, with optional OpenAI phrasing."""

    def __init__(self):
        data = json.loads(Path(config.KB_PATH).read_text(encoding="utf-8"))
        self.intents = [i for i in data["intents"] if i["tag"] not in config.SKIP_TAGS]

        # One searchable row per pattern, plus one per response (helps keyword matches)
        rows, owners = [], []
        for idx, it in enumerate(self.intents):
            for p in it["patterns"]:
                rows.append(p)
                owners.append(idx)
            rows.append(it["responses"][0])
            owners.append(idx)
        self.owners = owners
        self.tfidf = _Tfidf(rows)

        self.client = None
        if config.USE_OPENAI and config.OPENAI_API_KEY:
            from openai import OpenAI
            self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def retrieve(self, query, k=config.TOP_K):
        """Return [(intent, score)] best first; score = best matching row of that intent."""
        best = {}
        for row_idx, s in self.tfidf.scores(query).items():
            owner = self.owners[row_idx]
            if s > best.get(owner, 0):
                best[owner] = float(s)
        ranked = sorted(best.items(), key=lambda x: x[1], reverse=True)[:k]
        return [(self.intents[i], s) for i, s in ranked if s > 0]

    def _search(self, question, history):
        """Try the question alone; for short follow-ups also try it with the previous question."""
        hits = self.retrieve(question)
        if len(question.split()) < 6:
            prev = [m["content"] for m in history if m["role"] == "user"]
            if prev:
                ctx_hits = self.retrieve(f"{prev[-1]} {question}")
                if ctx_hits and (not hits or ctx_hits[0][1] > hits[0][1]):
                    return ctx_hits
        return hits

    def answer(self, question, history):
        hits = self._search(question, history)
        if not hits or hits[0][1] < config.MIN_SCORE:
            return {"answer": config.UNKNOWN_REPLY, "sources": [], "confidence": 0.0, "known": False}

        top, confidence = hits[0]
        sources = [top.get("source", "FUL chatbot dataset 2026")]

        # Small talk and strong matches don't need an API call
        if top["tag"] in config.SMALLTALK_TAGS and confidence >= config.SMALLTALK_SCORE:
            return {"answer": random.choice(top["responses"]), "sources": [], "confidence": confidence, "known": True}

        if not self.client:
            return {"answer": random.choice(top["responses"]), "sources": sources, "confidence": confidence, "known": True}

        context = "\n\n".join(f"[{it['tag']}] {it['responses'][0]}" for it, _ in hits)
        messages = [{
            "role": "system",
            "content": (
                "You are the Federal University Lokoja (FUL) information assistant. "
                "Answer ONLY from the context below. Be concise and friendly. "
                "Never invent fees, dates, names or requirements. If the context does not "
                f"answer the question, reply exactly: {config.UNKNOWN_REPLY}\n\nContext:\n{context}"
            ),
        }]
        messages += [{"role": m["role"], "content": m["content"]} for m in history[-6:]]
        messages.append({"role": "user", "content": question})
        resp = self.client.chat.completions.create(
            model=config.OPENAI_MODEL, messages=messages, temperature=0.2
        )
        text = resp.choices[0].message.content.strip()
        known = text != config.UNKNOWN_REPLY
        return {"answer": text, "sources": sources if known else [], "confidence": confidence, "known": known}

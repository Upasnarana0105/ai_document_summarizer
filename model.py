import os, re
from collections import Counter

# Lightweight text extraction helpers and naive NLP fallbacks.
# This file avoids forcing heavy dependencies. If you want better results, install:
# transformers, torch, sentencepiece, spacy, nltk and replace the fallback functions
# with model-backed implementations.

def extract_text_from_file(path):
    """Extract text from a PDF or txt file. Uses PyPDF2 if available, else very naive fallback."""
    ext = path.rsplit('.', 1)[-1].lower()
    if ext == 'txt':
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    # Try PDF extraction using PyPDF2 if installed
    try:
        import PyPDF2
        text = []
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for p in reader.pages:
                t = p.extract_text() or ''
                text.append(t)
        return '\n'.join(text)
    except Exception as e:
        # naive fallback: return empty string so caller knows extraction failed
        return ''

def simple_sentences(text):
    # split into sentences via punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 20]

def naive_summarize(text, max_sentences=3):
    """A naive summarizer: score sentences by word frequency (simple) and return top sentences."""
    sentences = simple_sentences(text)
    if not sentences:
        # fallback: return beginning of text
        return ' '.join(text.split()[:80])

    # build word frequencies
    words = re.findall(r'\w+', text.lower())
    stopwords = set(["the","and","is","in","to","of","a","that","it","for","on","with","as","this","are","an","be"])
    freqs = Counter([w for w in words if w not in stopwords])
    # score sentences
    scored = []
    for s in sentences:
        s_words = re.findall(r'\w+', s.lower())
        score = sum(freqs.get(w,0) for w in s_words)
        scored.append((score, s))
    scored.sort(reverse=True)
    top = [s for _, s in scored[:max_sentences]]
    # preserve original order
    top_sorted = [s for s in sentences if s in top]
    return ' '.join(top_sorted)

def extract_keywords(text, top_k=10):
    words = re.findall(r'\w+', text.lower())
    stopwords = set(["the","and","is","in","to","of","a","that","it","for","on","with","as","this","are","an","be"])
    freqs = Counter([w for w in words if w not in stopwords and len(w)>2])
    common = [w for w,_ in freqs.most_common(top_k)]
    return common

def simple_sentiment(text):
    # very naive polarity: positive/negative by word lists
    pos = set(['good','great','excellent','positive','success','improve','benefit','happy','well','better'])
    neg = set(['bad','poor','fail','failure','negative','problem','issue','worse','wrong','concern'])
    words = set(re.findall(r'\w+', text.lower()))
    score = sum(1 for w in words if w in pos) - sum(1 for w in words if w in neg)
    if score > 0:
        return 'Positive'
    if score < 0:
        return 'Negative'
    return 'Neutral'

def generate_title(text, max_words=6):
    # naive title: take the most common nouns/keywords and join
    kws = extract_keywords(text, top_k=6)
    return ' '.join(kws[:max_words]).title() or 'Document Summary'

def extract_key_sentences(text, top_k=5):
    sentences = simple_sentences(text)
    if not sentences:
        return []
    # use same scoring as summarizer
    words = re.findall(r'\w+', text.lower())
    stopwords = set(["the","and","is","in","to","of","a","that","it","for","on","with","as","this","are","an","be"])
    freqs = Counter([w for w in words if w not in stopwords])
    scored = [(sum(freqs.get(w,0) for w in re.findall(r'\w+', s.lower())), s) for s in sentences]
    scored.sort(reverse=True)
    return [s for _, s in scored[:top_k]]

def generate_insights(text):
    summary = naive_summarize(text, max_sentences=3)
    keywords = extract_keywords(text, top_k=10)
    sentiment = simple_sentiment(text)
    title = generate_title(text)
    highlights = extract_key_sentences(text, top_k=5)
    return {
        'summary': summary,
        'keywords': keywords,
        'sentiment': sentiment,
        'auto_title': title,
        'highlights': highlights
    }

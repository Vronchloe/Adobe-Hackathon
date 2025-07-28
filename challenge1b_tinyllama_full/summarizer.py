from nltk.tokenize import sent_tokenize

def summarize_text(text, num_sentences=2):
    sentences = sent_tokenize(text)
    return " ".join(sentences[:num_sentences])

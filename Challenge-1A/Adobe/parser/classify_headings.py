import os, joblib, pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = "model/heading_model.pkl"

def is_valid_model(path):
    try:
        with open(path, 'rb') as f:
            pickle.load(f)
        return True
    except: return False

def train_model(features, labels):
    le = LabelEncoder()
    y = le.fit_transform(labels)
    X = [[f['size'], f['bold'], f['y0'], len(f['text'])] for f in features]
    clf = DecisionTreeClassifier(max_depth=5)
    clf.fit(X, y)
    joblib.dump((clf, le), MODEL_PATH)
    return clf, le

def classify_headings(elements):
    valid = os.path.exists(MODEL_PATH) and is_valid_model(MODEL_PATH)
    if not valid:
        labels = []
        for el in elements:
            wc = len(el['text'].split())
            if el['size'] >= 18 and wc <= 6:
                labels.append("H1")
            elif el['size'] >= 14 and wc <= 10:
                labels.append("H2")
            elif el['size'] >= 12 and wc <= 14:
                labels.append("H3")
            else:
                labels.append("P")
        clf, le = train_model(elements, labels)
    else:
        clf, le = joblib.load(MODEL_PATH)

    X = [[el['size'], el['bold'], el['y0'], len(el['text'])] for el in elements]
    y_pred = clf.predict(X)
    labels = le.inverse_transform(y_pred)

    result, title = [], None
    for el, label in zip(elements, labels):
        if label.startswith("H"):
            result.append({"level": label, "text": el['text'], "page": el['page']})
            if label == "H1" and not title:
                title = el['text']
    return result, title or "Untitled"
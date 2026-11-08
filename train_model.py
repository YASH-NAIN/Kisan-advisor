"""Train the leaf-image classifier (classical ML: features + Random Forest).
Run:  python train_model.py            (uses ./dataset)
Saves models/leaf_rf.joblib and prints accuracy + confusion matrix."""
import os, sys, joblib, numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from features import extract

root = sys.argv[1] if len(sys.argv) > 1 else "dataset"
X, y = [], []
classes = sorted(os.listdir(root))
for ci, c in enumerate(classes):
    for f in os.listdir(os.path.join(root, c)):
        X.append(extract(Image.open(os.path.join(root, c, f))))
        y.append(ci)
X, y = np.array(X), np.array(y)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
clf = RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=42).fit(Xtr, ytr)
pred = clf.predict(Xte)
print(classification_report(yte, pred, target_names=classes))
print(confusion_matrix(yte, pred))
os.makedirs("models", exist_ok=True)
joblib.dump({"model": clf, "classes": classes}, "models/leaf_rf.joblib")

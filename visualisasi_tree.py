import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder

# === LOAD DATA ===
data = pd.read_csv("data/siswa.csv")

# === ENCODING ===
le_gaya = LabelEncoder()
le_kemampuan = LabelEncoder()

data["gaya_belajar"] = le_gaya.fit_transform(data["gaya_belajar"])
data["kemampuan"] = le_kemampuan.fit_transform(data["kemampuan"])

# === FITUR & LABEL ===
X = data[["nilai_pretest", "gaya_belajar"]]
y = data["kemampuan"]

# === TRAIN MODEL ===
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X, y)

# === VISUALISASI POHON KEPUTUSAN ===
plt.figure(figsize=(16, 8))
plot_tree(
    model,
    feature_names=["nilai_pretest", "gaya_belajar"],
    class_names=le_kemampuan.classes_,
    filled=True,
    rounded=True
)
plt.title("Visualisasi Decision Tree - AI Pembelajaran Adaptif")
plt.show()

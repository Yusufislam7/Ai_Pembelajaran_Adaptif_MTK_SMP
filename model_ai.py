import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# === 1. LOAD DATA (AI BELAJAR) ===
data = pd.read_csv("data/siswa.csv")

# === 2. ENCODING ===
le_gaya = LabelEncoder()
le_kemampuan = LabelEncoder()

data["gaya_belajar"] = le_gaya.fit_transform(data["gaya_belajar"])
data["kemampuan"] = le_kemampuan.fit_transform(data["kemampuan"])

# === 3. FITUR & LABEL ===
X = data[["nilai_pretest", "gaya_belajar"]]
y = data["kemampuan"]

# === 4. TRAINING (AI LEARNING) ===
model = DecisionTreeClassifier(
    max_depth=3,
    random_state=42
)
model.fit(X, y)

# === 5. PREDIKSI (AI DIPAKAI) ===
def prediksi_kemampuan(nilai, gaya):
    gaya_encoded = le_gaya.transform([gaya])

    data_baru = pd.DataFrame(
        [[nilai, gaya_encoded[0]]],
        columns=["nilai_pretest", "gaya_belajar"]
    )

    hasil = model.predict(data_baru)
    return le_kemampuan.inverse_transform(hasil)[0]

if __name__ == "__main__":
    print("Tes AI:")
    print(prediksi_kemampuan(70, "visual"))

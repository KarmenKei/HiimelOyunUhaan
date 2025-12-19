import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

df = pd.read_csv("imdb_movies.csv")

df = df.rename(columns={
    "Rating": "imdb_score",
    "Genre": "genres",
    "Revenue (Millions)": "revenue"
})

df["successful"] = (df["imdb_score"] > 7).astype(int)

df = df.dropna(subset=["genres", "revenue", "imdb_score", "successful"])

X_genre = df["genres"].str.get_dummies(sep=",")
X_num = df[["revenue"]]

X = pd.concat([X_genre, X_num], axis=1)
y = df["successful"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=23,
    stratify=y
)

clf = DecisionTreeClassifier(
    criterion="entropy",
    max_depth=5,
    min_samples_leaf=10,
    random_state=23
)
clf.fit(X_train, y_train)

print("Train accuracy:", clf.score(X_train, y_train))
print("Test accuracy:", clf.score(X_test, y_test))

root_feature = X.columns[clf.tree_.feature[0]]
root_threshold = clf.tree_.threshold[0]
print("Root feature:", root_feature)
print("Root threshold:", round(root_threshold, 2))

plt.figure(figsize=(22, 10), dpi=150)
plot_tree(
    clf,
    feature_names=X.columns,
    class_names=["Unsuccessful", "Successful"],
    filled=True,
    rounded=True,
    fontsize=9,
    precision=2,
    proportion=True
)
plt.title("Decision Tree using Entropy (Lab 4)", fontsize=14)
plt.tight_layout()
plt.show()
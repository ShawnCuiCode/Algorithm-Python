import pandas as pd

def read_demo():
    # df = pd.read_csv("/Users/lanzy/Downloads/student+performance/student/student-mat.csv", sep=";")
    # df.columns = df.columns.str.strip()
    # print(df)
    # print(df.head())
    # print(df.iloc[1])
    # print(df.columns)
    # print(df[df["age"] > 10].head())
    # print(df[df['age'] >10])
    # print(df.max())
    # print(df.describe())

    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
    column_names = [
        "mpg", "cylinders", "displacement", "horsepower",
        "weight", "acceleration", "model year", "origin", "car name"
    ]

    df = pd.read_csv(url, names=column_names, delim_whitespace=True, na_values="?")

    print(df.head())
    print(df.info())

if __name__ == "__main__":
    read_demo()

import pandas as pd


# Path to original ARFF dataset
input_file = "autism+screening+adult/Autism-Adult-Data.arff"

# Output file
output_file = "data/asd_training.csv"


# -------------------------------------------------
# 1. Find the @data section
# -------------------------------------------------

with open(input_file, "r", encoding="utf-8") as file:
    lines = file.readlines()


data_start = None

for i, line in enumerate(lines):
    if line.strip().lower() == "@data":
        data_start = i + 1
        break


if data_start is None:
    raise ValueError("@data section not found in ARFF file")


# -------------------------------------------------
# 2. Read only the data section
# -------------------------------------------------

data_lines = []

for line in lines[data_start:]:

    line = line.strip()

    if line == "":
        continue

    if line.startswith("%"):
        continue

    data_lines.append(line)


# -------------------------------------------------
# 3. Define required columns
# -------------------------------------------------

columns = [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9",
    "A10",
    "Age",
    "gender",
    "ethnicity",
    "jundice",
    "austim",
    "contry_of_res",
    "used_app_before",
    "result",
    "age_desc",
    "relation",
    "Class"
]


# -------------------------------------------------
# 4. Convert raw data into DataFrame
# -------------------------------------------------

rows = []

for line in data_lines:

    # ARFF data is comma-separated
    values = line.split(",")

    if len(values) != len(columns):
        print("Skipping invalid row:")
        print(line)
        continue

    rows.append(values)


df = pd.DataFrame(rows, columns=columns)


# -------------------------------------------------
# 5. Keep only ML features
# -------------------------------------------------

df = df[
    [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
        "A10",
        "Age",
        "Class"
    ]
]


# -------------------------------------------------
# 6. Convert numeric columns
# -------------------------------------------------

numeric_columns = [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9",
    "A10",
    "Age"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# -------------------------------------------------
# 7. Clean missing values
# -------------------------------------------------

print("\nMissing values before cleaning:")
print(df.isnull().sum())


df = df.dropna()


# -------------------------------------------------
# 8. Remove invalid age values
# -------------------------------------------------

df = df[
    (df["Age"] >= 1) &
    (df["Age"] <= 100)
]


# -------------------------------------------------
# 9. Convert target
# -------------------------------------------------

df["Class"] = df["Class"].str.strip()

df["Class"] = df["Class"].map({
    "YES": 1,
    "NO": 0
})


# Remove rows with invalid target
df = df.dropna(subset=["Class"])


# Convert target to integer
df["Class"] = df["Class"].astype(int)


# -------------------------------------------------
# 10. Convert feature values to integer
# -------------------------------------------------

for column in numeric_columns:
    df[column] = df[column].astype(int)


# -------------------------------------------------
# 11. Save processed dataset
# -------------------------------------------------

df.to_csv(
    output_file,
    index=False
)


# -------------------------------------------------
# 12. Display information
# -------------------------------------------------

print("\n======================================")
print("DATASET PROCESSING COMPLETE")
print("======================================")

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nClass distribution:")
print(df["Class"].value_counts())

print("\nSaved to:")
print(output_file)
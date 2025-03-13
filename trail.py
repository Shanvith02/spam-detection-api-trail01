import pandas as pd

df = pd.read_csv("spam.csv", encoding="latin-1", usecols=[0, 1])
df.columns = ['label', 'message']

# Count spam and ham messages
print(df['label'].value_counts())

import pandas as pd

# Read the CSV Files 
df = pd.read_csv('domains.csv')

# Remove the rows with spaces in the word column
df=df[df['word'].str.contains(' ')==False]

# Remove the rows with hyphen in the word column
df=df[df['word'].str.contains('-')==False]

# print row and column count
print(df.shape)

print(df.head(100))
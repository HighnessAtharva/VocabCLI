import pandas as pd

df = pd.read_csv('domains.csv') # Read the CSV Files 
df=df[df['word'].str.contains(' ')==False] # Remove the rows with spaces in the word column
df=df[df['word'].str.contains('-')==False] # Remove the rows with hyphen in the word column
df=df[df['word'].str.contains('\'')==False] # Remove the rows with apostrophe in the word column
df=df.drop(df[(df['word']==df['topic'])].index) # drop rows where word column and topic column have same value
df=df.drop_duplicates(subset='word') # Remove duplicate rows
df=df.sort_values(by=['topic', 'word']) # sort the dataframe by topic and word
df.reset_index(drop=True, inplace=True) # reset index

# delete words if length is less than 3
for i in range(len(df)):
    if len(df['word'][i])<=2:
        df.drop(i, inplace=True)

        
print(df.shape) # print row and column count
print(df.groupby('topic').count().sort_values(['word'],ascending=False)) # show word count grouped by topic and sorted by word count

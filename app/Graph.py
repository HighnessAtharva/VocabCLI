# import libraries
import seaborn as sns
import matplotlib.pyplot as plt 
import pandas as pd
from modules.Database import *



# function to visualize top N tags with the most words
def viz_top_tags(N=10):
    # get top N tags
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT tag, COUNT(*) FROM words WHERE tag is NOT NULL GROUP BY tag ORDER BY COUNT(*) DESC LIMIT ?", (N,))
    rows=c.fetchall()

    top_tags=[row[0] for row in rows if row[0] is not None]
    count= [row[1] for row in rows if row[1] != 0]
    
    if not top_tags:
        print("No tags found")
        return
    
    if len(top_tags) < N:
        print("Not enough tags found. Showing graph for available tags only.")
    
    # create a dataframe
    df = pd.DataFrame(list(zip(top_tags, count)), index=count, columns=['Tag', 'Count'])

    # plot the dataframe
    graph=sns.barplot(x='Tag', y='Count', data=df, palette='pastel')

    # set the title
    graph.set(title=f'Top {N} Tags', xlabel='Tags', ylabel='Count')
    plt.figure(figsize=(10,5), tight_layout=True)


    # show the plot
    plt.show()
    
viz_top_tags()

# todo function to visualize top distribution of words by date [day, week, month]

# todo function to vizualize trend of learning and mastered words in a given time period [day, week, month] -> USE COMPOSITE BAR GRAPH

# todo function to visualize most looked up words [top 10] with the number of times looked up


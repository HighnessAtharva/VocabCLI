from Database import *
import calendar
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from datetime import datetime
from rich.panel import Panel




################################
# GRAPH CAROUSEL
################################

import tkinter as Tk
from tkinter import ttk
from PIL import Image, ImageTk
import glob


<<<<<<< Updated upstream


def show_all_graphs():
    height = 700 # Window height
    width = 1300 # Window Width

    def show(event):
        print(event.x,event.y)



    class TKApp(Tk.Tk):
        def __init__(self,title):
            super().__init__()

            # App Sizing and Title
            geometry = f'{width}x{height}'
            self.geometry(geometry)
            self.title(title)
            self.resizable(0,0)

            self.bind('<Left>',moveImageLeft)
            self.bind('<Right>',moveImageRight)




    class Carousel(Tk.Canvas):
        def __init__(self,master):
            super().__init__()
            self.config(width=width,height=height)
            self.pack()
            self.stitchImages()
            self.showPhoto()
            self.loadIndicator()
            self.current = 1


        def stitchImages(self):
            # Stitch Image
            images = [Image.open(file) for file in glob.glob('../exports/*.jpg')]
            widths, heights = zip(*(i.size for i in images))
            total_width = sum(widths)
            max_height = max(heights)
            self.stitched = Image.new('RGB', (total_width, max_height))
            x_offset = 0
            for im in images:
                self.stitched.paste(im, (x_offset,0))
                x_offset += im.size[0]
            self.stitched = self.stitched.resize((len(images)*1300,700))
            self.length = len(images)

        def showPhoto(self):
            # Show Stitched Image
            self.stitched = ImageTk.PhotoImage(self.stitched)
            self.Photo = self.create_image((0,0),image=self.stitched,anchor='nw')


        def loadIndicator(self):
            # Indicator
            self.ind = self.create_rectangle(1,690,310,700,fill='white',outline='white')

        def move_util(self, arg0, arg1):
            self.after(1, self.move(self.Photo, arg0, 0))
            self.after(1, self.move(self.ind, arg1, 0))
            self.update()

        def moveImageRight(self):
            if self.current < 4:
                for _ in range(25):
                    # first argument is the number of pixels to move the image
                    # second argument is the number of pixels to move the indicator
                    self.move_util(-52, 15)
                self.current += 1

        def moveImageLeft(self):
            if self.current > 0:
                for _ in range(25):
                    # first argument is the number of pixels to move the image
                    # second argument is the number of pixels to move the indicator
                    self.move_util(52, -15)
                self.current -= 1

        img_index = None

    def moveImageRight(event):
        global img_index
        if img_index.current != 4:
            img_index.moveImageRight()

    def moveImageLeft(event):
        global img_index
        if img_index.current != 1:
            img_index.moveImageLeft()

    def start_carousel():
        global img_index
        tk_app = TKApp('Graphs')
        img_index = Carousel(tk_app)
        tk_app.mainloop()

    start_carousel()

=======
height = 700 # Window height
width = 1300 # Window Width

def show(event):
    print(event.x,event.y)

class TKApp(Tk.Tk):
    def __init__(self,title):
        super().__init__()

        # App Sizing and Title
        geometry = f'{str(width)}x{str(height)}'
        self.geometry(geometry)
        self.title(title)
        self.resizable(0,0)

        self.bind('<Left>',moveImageLeft)
        self.bind('<Right>',moveImageRight)


class Carousel(Tk.Canvas):
    def __init__(self,master):
        super().__init__()
        self.config(width=width,height=height)
        self.pack()
        self.stitchImages()
        self.showPhoto()
        self.loadIndicator()
        self.current = 1


    def stitchImages(self):
        # Stitch Image
        images = [Image.open(file) for file in glob.glob('files/*.jpg')]
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)
        self.stitched = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for im in images:
          self.stitched.paste(im, (x_offset,0))
          x_offset += im.size[0]
        self.stitched = self.stitched.resize((len(images)*1300,700))
        self.length = len(images)

    def showPhoto(self):
        # Show Stitched Image
        self.stitched = ImageTk.PhotoImage(self.stitched)
        self.Photo = self.create_image((0,0),image=self.stitched,anchor='nw')


    def loadIndicator(self):
        # Indicator
        self.ind = self.create_rectangle(1,690,310,700,fill='white',outline='white')

    def move_util(self, arg0, arg1):
        self.after(1, self.move(self.Photo, arg0, 0))
        self.after(1, self.move(self.ind, arg1, 0))
        self.update()
        
    def moveImageRight(self):
        if self.current < 4:
            for _ in range(25):
                # first argument is the number of pixels to move the image
                # second argument is the number of pixels to move the indicator
                self.move_util(-52, 15)
            self.current += 1

    def moveImageLeft(self):
        if self.current > 0:
            for _ in range(25):
                # first argument is the number of pixels to move the image
                # second argument is the number of pixels to move the indicator
                self.move_util(52, -15)
            self.current -= 1


img_index = None

def moveImageRight(event):
    global img_index
    if img_index.current != 4:
        img_index.moveImageRight()

def moveImageLeft(event):
    global img_index
    if img_index.current != 1:
        img_index.moveImageLeft()

def start_carousel():
    global img_index
    tk_app = TKApp('Graphs')
    img_index = Carousel(tk_app)
    tk_app.mainloop()

start_carousel()
>>>>>>> Stashed changes


################################
# VISUALIZATION FUNCTIONS
################################
def viz_top_words_bar(N=10):
    """_summary_

    Args:
        N (int, optional): _description_. Defaults to 10.
    """
    
    # get top N words
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT word, COUNT(*) FROM words GROUP BY word ORDER BY COUNT(*) DESC LIMIT ?", (N,))
    rows=c.fetchall()

    top_words=[row[0] for row in rows if row[0] is not None]
    count= [row[1] for row in rows if row[1] != 0]

    if not top_words:
        print(Panel("No tags found"))
        return

    if len(top_words) < N:
        print(Panel("Not enough words found. Showing graph for available words only."))

    # create a dataframe
    df = pd.DataFrame(list(zip(top_words, count)), index=count, columns=['Word Lookup Count', 'Count'])

    sns.set_style("dark")

    # plot the dataframe
    graph=sns.barplot(x='Word Lookup Count', y='Count', data=df, palette='pastel',ax=plt.subplots(figsize=(12, 10))[1], edgecolor='0.4')

    graph.set_title(f'Top {N} Most Looked Up Words', fontsize=18, fontweight='bold', pad=20, color='black', loc='center', fontname='Constantia') 
    graph.set_xlabel('Words', fontsize=15, fontweight='bold', labelpad=-10, color='black', fontname='MS Gothic')
    graph.set_ylabel('Lookup Count', fontsize=15, fontweight='bold', labelpad=20, color='black', fontname='MS Gothic')
    graph.set_xticklabels(graph.get_xticklabels(), rotation=40, ha="right", fontname='Candara', color='black', fontweight='700')
    graph.set_yticklabels(graph.get_yticklabels(), fontname='Candara',color='black')

    # show the plot
    plt.grid()
    plt.show()


def viz_top_tags_bar(N=10):
    """
    Visualizes the top N tags with the most words.

    Args:
        N (int, optional): Number of top tags to visualize . Defaults to 10.
    """

    # get top N tags
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT tag, COUNT(*) FROM words WHERE tag is NOT NULL GROUP BY tag ORDER BY COUNT(*) DESC LIMIT ?", (N,))
    rows=c.fetchall()

    top_tags=[row[0] for row in rows if row[0] is not None]
    count= [row[1] for row in rows if row[1] != 0]

    if not top_tags:
        print(Panel("No tags found"))
        return

    if len(top_tags) < N:
        print(Panel("Not enough tags found. Showing graph for available tags only."))

    # create a dataframe
    df = pd.DataFrame(list(zip(top_tags, count)), index=count, columns=['Tag', 'Count'])

    sns.set_style("dark")

    # plot the dataframe
    graph=sns.barplot(x='Tag', y='Count', data=df, palette='pastel',ax=plt.subplots(figsize=(12, 10))[1], edgecolor='0.4')

    
    graph.set_title(f'Top {N} Tags', fontsize=18, fontweight='bold', pad=20, color='black', loc='center', fontname='Constantia') 
    graph.set_xlabel('Tags', fontsize=15, fontweight='bold', labelpad=-8, color='black', fontname='MS Gothic') 
    graph.set_ylabel('Word Count',fontsize=15, fontweight='bold', labelpad=20, color='black', fontname='MS Gothic')
    graph.set_xticklabels(graph.get_xticklabels(), rotation=40, ha="right", fontname='Candara', color='black')
    graph.set_yticklabels(graph.get_yticklabels(), fontname='Candara',color='black')

    # show the plot
    plt.grid()
    plt.show()


def viz_top_words_pie(N=10):
    print("Will print a pie chart of the top N words")
    
def viz_top_tags_pie(N=10):
    print("Will print a pie chart of the top N tags")


def words_distribution_week_util():
    """
    Returns the distribution of words by day of the week.

    Returns:
        list: list of days of the week.
        list: list of days of the word counts.
    """

    conn=createConnection()
    c=conn.cursor()

    days={0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

    days_of_week=[None]*7
    word_count=[None]*7

    # get word count for each day in current week
    c.execute("select strftime('%d/%m/%Y', datetime) as date, count(word) from words WHERE datetime>=datetime('now', '-7 days') GROUP BY date")

    rows=c.fetchall()
    for index, row in enumerate(rows):
        date=datetime.strptime(row[0], "%d/%m/%Y")
        days_of_week[index]=days.get(date.weekday())
        word_count[index]=row[1]

    return days_of_week, word_count

def viz_word_distribution_week():
    """ Visualizes the distribution of words by day of the week. """

    days_of_week, word_count=words_distribution_week_util()

    # create a dataframe
    df = pd.DataFrame(list(zip(days_of_week, word_count)),  columns=['Day', 'Count'])

    sns.set_style("dark")
    # plot the dataframe
    graph=sns.barplot(x='Day', y='Count', data=df, palette='pastel', ax=plt.subplots(figsize=(12, 10))[1], edgecolor='0.4')

    graph.set_title('Words Distribution by Week', fontsize=18, fontweight='bold', pad=20, color='black', loc='center', fontname='Constantia') 
    graph.set_xlabel('Day', fontsize=15, fontweight='bold', labelpad=10, color='black', fontname='MS Gothic')
    graph.set_ylabel('Count', fontsize=15, fontweight='bold', labelpad=20, color='black', fontname='MS Gothic')
    graph.set_xticklabels(graph.get_xticklabels(), fontname='Candara', color='black')
    graph.set_yticklabels(graph.get_yticklabels(), fontname='Candara',color='black')
    
    plt.grid()
    plt.show()



def word_distribution_month_util():
    """
    Returns the distribution of word by dates of month.

    Returns:
        list: List of dates of month.
        list: List of word counts.
    """

    conn=createConnection()
    c=conn.cursor()

    # determine current year, current month and next month [INT]
    year=datetime.now().year
    month=datetime.now().month
    month_next=datetime.now().month+1
    if month_next==13:
        month_next=1
        increment_year=True

    # determine total number of days in current month [INT]
    total_days=calendar.monthrange(year, month)[1]
    word_count=[None]*total_days

    # get unformatted datestrings for each day in current month
    current_month = f"{str(year)}-{str(month)}"
    if len(str(month_next))==1:
        month_next=f"0{str(month_next)}"
    next_month = f"{str(year+1 if increment_year else year)}-{str(month_next)}"
    #todo print(current_month, next_month)
    dates=np.arange(current_month, next_month, dtype='datetime64[D]').tolist()
    
    dates=[date.strftime("%d %b, %Y") for date in dates]
    
    # get word count for each day in current month
    c.execute("select strftime('%d', datetime) as date, count(word) as word_count from words WHERE date(datetime)>=date('now', 'start of month') GROUP BY date")
    rows=c.fetchall()
    for row in rows:
        index=int(row[0])-1
        word_count[index]=row[1]

    return dates, word_count


def viz_word_distribution_month():
    """ Visualizes the distribution of words by dates of month. """

    dates, word_count=word_distribution_month_util()
    # print(dates)

    # create a dataframe
    df = pd.DataFrame(list(zip(dates, word_count)),  columns=['Date', 'Count'])

    sns.set_style("dark")
    # plot the dataframe
    graph=sns.barplot(x='Date', y='Count', data=df, palette='pastel', ax=plt.subplots(figsize=(12, 8))[1], edgecolor='0.4')


    graph.set_title('Word Distribution by Month', fontsize=18, fontweight='bold', pad=5, color='black', loc='center', fontname='Constantia') 
    graph.set_xlabel('Date', fontsize=15, fontweight='bold', labelpad=0, color='black', fontname='MS Gothic')
    graph.set_ylabel('Count', fontsize=15, fontweight='bold', labelpad=20, color='black', fontname='MS Gothic')
    graph.set_xticklabels(graph.get_xticklabels(), rotation=40, ha="right",fontname='Candara', color='black')
    graph.set_yticklabels(graph.get_yticklabels(), fontname='Candara',color='black')
    
    plt.tight_layout()
    plt.grid()
    plt.show()


def viz_word_distribution_year_util():
    pass

def viz_word_distribution_year():
    pass

def viz_learning_vs_mastered():
    """ Visualizes the distribution of words by learning and mastered. """    
    conn=createConnection()
    c=conn.cursor()
    
    c.execute("select count(DISTINCT word) from words WHERE learning = 1")
    learning_count=c.fetchone()[0]
    
    c.execute("select count(DISTINCT word) from words WHERE mastered = 1")
    mastered_count=c.fetchone()[0]
    
    print(learning_count, mastered_count)
    # set plot style: grey grid in the background:
    sns.set(style="dark")

    # set the figure size
    plt.figure(figsize=(14, 14))

    # top bar -> sum all values(learning and mastered) to find y position of the bars
    top_bar = [learning_count]
    bottom_bar = [mastered_count]
    
    x = ['']
    plt.bar(x, bottom_bar, color='darkblue')
    plt.bar(x, top_bar, bottom=bottom_bar, color='lightblue')

    # add legend
    top_bar = mpatches.Patch(color='darkblue', label='mastered words')
    bottom_bar = mpatches.Patch(color='lightblue', label='learning words')
    plt.legend(handles=[top_bar, bottom_bar])

    plt.title('Word Distribution by Month', fontsize=18, fontweight='bold', pad=5, color='black', loc='center', fontname='Constantia') 
    plt.xlabel('Date', fontsize=15, fontweight='bold', labelpad=0, color='black', fontname='MS Gothic')
    plt.ylabel('Count', fontsize=15, fontweight='bold', labelpad=20, color='black', fontname='MS Gothic')
    
    # show the graph
    plt.show()

# todo function to vizualize trend of learning and mastered words in a given time period [day, week, month] -> USE COMPOSITE BAR GRAPH

# todo function to visualize most looked up words [top 10] with the number of times looked up


# Graph of application usage time over various time periods [week, month, year] Need Research
# Graph of words mastered over various time periods [week, month, year] In Consideration
# Graph of time taken to master words after first lookup/ set learning over various time periods [week, month, year] In Consideration
# Graph of words based on their frequency of lookup [top 10] with the number of times looked up ✅
# Graph of words based on their conceptual category (if possible with the libraries) ✅
# Graph related to complexity or difficulty? ✅
# Can show graphs related to flashcards after implementing them? ✅

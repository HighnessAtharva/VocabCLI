from PIL import Image, ImageDraw, ImageFont
from Database import createConnection
from Dictionary import *
import json

def export_util(c,query:str):
    # Create a new image with a white background
    width, height = 1080, 1080
    image = Image.new('RGB', (width, height), 'white')

    # Get a drawing context
    draw = ImageDraw.Draw(image)

    # Draw a gradient from red to blue
    for i in range(height):
        # Calculate the current intensity of red and blue
        red = int(i / height * 255)
        blue = 0 - red
        
        # Draw a line with the current color
        draw.line((0, i, width, i), fill=(red, 0, blue))


    # Use ImageFont to specify the font and size of the text
    font = ImageFont.truetype('arial.ttf', 32)
    wordfont = ImageFont.truetype('arial.ttf', 64)
    
    c.execute("SELECT api_response FROM cache_words WHERE word=?", (query,))
    definition=json.loads(c.fetchone()[0])

    # Draw the word and its definition on the image
    draw.text((50, 50), word, fill='white', font=wordfont)
    # if word is favorite
    draw.text((250, 50), "💙", fill='white', font=font)
    # if word is mastered 
    draw.text((250, 50), "✅", fill='white', font=font)
    # if word is learning
    draw.text((250, 50), "⏳", fill='white', font=font)
    
    # check if the word has any tag
    c.execute("SELECT tag FROM words WHERE word=?",(word,))
    tag=c.fetchone()
    if tag:
        tag=tag[0]
        draw.text((50, 100), tag, fill='white', font=font)

    draw.text((50, 150), definition, fill='white', font=font)

    # Save the image
    image.save(word+'.png')


def export_all():
    conn=createConnection()
    c=conn.cursor()

    # Sql query to get all the words
    c.execute("SELECT * FROM words")
    words=c.fetchall()

    for word in words:
        export_util(c,word)



def export_mastered():
    conn=createConnection()
    c=conn.cursor()

    # sql query to get all the mastered words
    c.execute("SELECT * FROM words WHERE mastered=1")
    words=c.fetchall()

    for word in words:
        export_util(c,word)


def export_learning():
    conn=createConnection()
    c=conn.cursor()

    # sql query to get all the learning words
    c.execute("SELECT * FROM words WHERE learning=1")
    words=c.fetchall()

    for word in words:
        export_util(c,word)


def export_favorite():
    conn=createConnection()
    c=conn.cursor()

    # sql query to get all the favorite words
    c.execute("SELECT * FROM words WHERE favorite=1")
    words=c.fetchall()

    for word in words:
        export_util(c,word)
        

def export_tag(query:str):
    conn=createConnection()
    c=conn.cursor()

    # sql query to get all the words with the tag
    c.execute("SELECT * FROM words WHERE tag LIKE ?",(query,))
    words=c.fetchall()

    for word in words:
        export_util(c,word)


def export_word(query:str):
    conn=createConnection()
    c=conn.cursor()

    # sql query to get all the words with the word
    c.execute("SELECT * FROM words WHERE word LIKE ?",(query,))
    words=c.fetchall()

    for word in words:
        export_util(c,word)

export_all()
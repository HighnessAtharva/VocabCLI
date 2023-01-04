from PIL import Image, ImageDraw, ImageFont
from Database import createConnection
from Dictionary import *
import json
import textwrap



def flashcard_definition(query:str) -> str:
    # sourcery skip: use-contextlib-suppress
    """
    Docstring 
    """
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT api_response FROM cache_words WHERE word=?", (query,))
    
    
    response=c.fetchone()[0]
    response=json.loads(response)
    
    defs_and_examples = {}
    
    for meaningNumber in response["meanings"]:
        for count, meaning in enumerate(meaningNumber["definitions"][:3], start=1): # get only the first 3 meanings
            defs_and_examples[meaning["definition"]] = meaning["example"] if "example" in meaning else None 
            
    # return the first 3 definitions and examples 
    return {k: defs_and_examples[k] for k in list(defs_and_examples)[:3]}
   



def export_util(c, type:str):

    if not (rows := c.fetchall()):
            print(f"No words found for selected criteria: {type}")

    # Create a new image with a white background
    width, height = 1080, 1080

    for row in rows:
        tag = row[1] if type =="tag" else None
        word=row[0]
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
        emojifont = ImageFont.truetype('NotoColorEmoji.ttf',109)

        # Draw the word and its definition on the image
        draw.text((50, 50), word, fill='white', font=wordfont)
        # if word is favorite
        if type == "favorite":
            draw.text((250, 50), "💙",  embedded_color=True, font=emojifont)
        elif type == "learning":
            draw.text((250, 50), "⏳",  embedded_color=True, font=emojifont)
        elif type == "mastered":
            draw.text((250, 50), "✅" , embedded_color=True, font=emojifont)
        
        # check if the word has any tag
        if tag:
            draw.text((50, 100), tag, fill='white', font=font)

        # get the dictionary of definitions:examples
        def_and_example= flashcard_definition(word)
        for count, (definition, example) in enumerate(def_and_example.items(), start=1):
            definition = textwrap.fill(definition, width=65)
            linecount=0
            if example:
                example = textwrap.fill(example, width=65)
                linecount+=len(definition.splitlines())
                linecount+=len(example.splitlines())
                draw.text((50, 250+(count*linecount*50)), f"{count}. {definition}\n - {example}", fill='white', font=font)
            else:
                draw.text((50, 250), f"{count}. {definition}", fill='white', font=font)
                
                
        # Make a folder of the type of words
        # todo @atharva make a subfolder for each tag in tag folder, and all the folders in a folder called "flashcards"
        if not os.path.exists(f"{type}"):
            os.makedirs(f"{type}")

        # Save the image to a file
        image.save(f"{type}/{word}.png")
            
        
    
def export_all():
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words")
    export_util(c, type="all words")



def export_mastered():
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words WHERE mastered=1")
    export_util(c, type="mastered")


def export_learning():
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words WHERE learning=1")
    export_util(c, type="learning")


def export_favorite():
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words WHERE favorite=1")
    export_util(c, type="favorite")

        

def export_tag(query:str):
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT DISTINCT(word), tag FROM words WHERE tag=?", (query,))
    export_util(c, type="tag")


def export_word(query:str):
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words WHERE word=?", (query,))
    export_util(c, type="word")


export_mastered()
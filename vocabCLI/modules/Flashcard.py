from PIL import Image, ImageDraw, ImageFont
from .Database import createConnection
from .Dictionary import *
import json
import textwrap
import random
from rich.progress import track


def flashcard_definition(query: str) -> str:
    # sourcery skip: use-contextlib-suppress
    """
    Docstring 
    """
    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT api_response FROM cache_words WHERE word=?", (query,))

    response = c.fetchone()[0]
    response = json.loads(response)

    defs_and_examples = {}

    for meaningNumber in response["meanings"]:
        # get only the first 3 meanings
        for count, meaning in enumerate(meaningNumber["definitions"][:3], start=1):
            defs_and_examples[meaning["definition"]
                              ] = meaning["example"] if "example" in meaning else None

    # return the first 3 definitions and examples
    return {k: defs_and_examples[k] for k in list(defs_and_examples)[:3]}



def interpolate(black, random_color, interval):
    derandom_color =[(t - f) / interval for f , t in zip(black, random_color)]
    for i in range(interval):
        yield [round(t + det * i) for t, det in zip(black, derandom_color)]
        
        
def export_util(c, type: str):  # sourcery skip: low-code-quality

    if not (rows := c.fetchall()):
        print(f"No words found for selected criteria: {type}")

    # Create a new image with a white background
    width, height = 1080, 1080


    my_colors=[
       
       # shades of red
        (255,99,71),
        (255,127,80),
        (205,92,92),
        (240,128,128),
        (233,150,122),
        (250,128,114),
        (255,160,122),


        # shades of green
        (50,205,50),
        (144,238,144),
        (152,251,152),
        (143,188,143),
        (0,250,154),
        (0,255,127),


        # shades of blue
        (0,255,255),
        (224,255,255),
        (0,206,209),
        (64,224,208),
        (72,209,204),
        (175,238,238),
        (127,255,212),
        (176,224,230),
        (95,158,160),
        (70,130,180),
        (100,149,237),
        (0,191,255),
        (30,144,255),


        # shades of purple
        (106,90,205),
        (123,104,238),
        (147,112,219),
        (153,50,204),
        (186,85,211),
        (128,0,128),
        (216,191,216),
        (221,160,221),
        (238,130,238),
        (255,0,255),

        # shades of pink
        (199,21,133),
        (219,112,147),
        (255,20,147),
        (255,105,180),
        (255,182,193),
        (255,192,203)   
    ]
    

    progressbar_total=0
    
    #----------------- Progress Bar -----------------#
    
    for row, _ in zip(rows, track(range(len(rows)-1), description=" 🔃 Exporting Flashcards ")):
    
    #----------------- Progress Bar -----------------#
                
    

        tag = row[1] if type == "tag" else None
        word = row[0]
        image = Image.new('RGB', (width, height), 'white')

        # Get a drawing context
        draw = ImageDraw.Draw(image)
        
        black = (0,0,0)
        random_color = random.choice(my_colors)
        # print(random_color)
        for i, color in enumerate(interpolate(random_color, black, image.width * 2)):
            draw.line([(i, 0), (0, i)], tuple(color), width=1)
    
    
        # Use ImageFont to specify the font and size of the text
        font = ImageFont.truetype('../assets/FTLTLT.ttf', 32)
        headingfont = ImageFont.truetype('../assets/FTLTLT.ttf', 64)


        # draw the watermark in the top right corner
        watermark = Image.open("../assets/VocabCLI -  White.png")
        watermark = watermark.resize((200, 200))
        image.paste(watermark, (880, -50), mask=watermark)

        # Draw the word and its definition on the image
        draw.text((50, 50), word.upper(), fill='white', font=headingfont, stroke_width=2, stroke_fill="black")

        if type == "favorite":
            # paste the heart on the image at position (250, 50) with transparency
            heart = Image.open("../assets/heart.png")
            heart = heart.resize((50, 50))
            image.paste(heart, (50, 150), mask=heart)

        elif type == "learning":
            clock = Image.open("../assets/clock.png")
            clock = clock.resize((50, 50))
            image.paste(clock, (50, 150), mask=clock)

        elif type == "mastered":
            tick = Image.open("../assets/tick.png")
            tick = tick.resize((50, 50))
            image.paste(tick, (50, 150), mask=tick)

        # check if the word has any tag
        if tag:
            tagImg = Image.open("../assets/tag.png")
            tagImg = tagImg.resize((75, 75))
            image.paste(tagImg, (50, 125), mask=tagImg)
            
            draw.text((150, 150), tag, fill='white', font=font)

        # get the dictionary of definitions:examples
        def_and_example = flashcard_definition(word)
        

        for count, (definition, example) in enumerate(def_and_example.items(), start=1):
            definition = textwrap.fill(definition, width=65)
            y_pos = 150+(count*200)

            # if the definition has an example, add it to the flashcard
            if example:
                example = textwrap.fill(example, width=65)
                draw.text((50, y_pos),
                        f"{count}. {definition}\n eg. {example}", fill='black', font=font)
            else:
                draw.text((50, y_pos), f"{count}. {definition}", fill='black', font=font)
            
                
            
        # save images to their respective folders based on passed type
        if tag:
            if not os.path.exists(f"flashcard/tag/{tag}"):
                os.makedirs(f"flashcard/tag/{tag}")

            # Save the image to a file and overwrite it
            if os._exists(name := f"flashcard/tag/{tag}/{word}.png"):
                os.remove(name)
            image.save(f"flashcard/tag/{tag}/{word}.png")

        else:
            if not os.path.exists(f"flashcard/{type}"):
                os.makedirs(f"flashcard/{type}")

            # Save the image to a file and overwrite it
            if os._exists(name := f"flashcard/{type}/{word}.png"):
                os.remove(name)
            image.save(f"flashcard/{type}/{word}.png")
            
        progressbar_total += 1
                
        
            

def generate_all_flashcards():
    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words")
    export_util(c, type="all words")


def generate_mastered_flashcards():
    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words WHERE mastered=1")
    export_util(c, type="mastered")


def generate_learning_flashcards():
    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words WHERE learning=1")
    export_util(c, type="learning")


def generate_favorite_flashcards():
    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words WHERE favorite=1")
    export_util(c, type="favorite")


def generate_tag_flashcards(query: str):
    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT(word), tag FROM words WHERE tag=?", (query,))
    export_util(c, type="tag")


# def export_word(query: str):
#     conn = createConnection()
#     c = conn.cursor()
#     c.execute("SELECT DISTINCT(word) FROM words WHERE word=?", (query,))
#     export_util(c, type="word")
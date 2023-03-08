import json
import random
import textwrap

from Database import createConnection
from Dictionary import *
from PIL import Image, ImageDraw, ImageFont
from rich.progress import track


def flashcard_definition(query: str) -> str:
    # sourcery skip: use-contextlib-suppress
    """
    Returns the definition of the word from the cache.

    1. Execute a query that selects the api_response column from the cache_words table where the word column is equal to the query
    2. Load the api_response column as a JSON object
    3. Create an empty dictionary
    4. Loop through each meaning in the meanings array
    5. For each meaning, loop through the first 3 definitions
    6. For each definition, add it to the dictionary with the key being the definition and the value being the example if it exists
    7. Return the first 3 definitions and examples

    Args:
        query (str): The word to be searched

    Returns:
        str: The definition of the word
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
            defs_and_examples[meaning["definition"]] = (
                meaning["example"] if "example" in meaning else None
            )

    # return the first 3 definitions and examples
    return {k: defs_and_examples[k] for k in list(defs_and_examples)[:3]}


def interpolate(random_color2, random_color, interval):
    """
    Interpolate between two colors.

    1. It calculates the difference between the two colors
    2. It divides the difference by the number of steps
    3. It adds the difference to the black color each time it moves one step
    4. It returns the new color, rounded to the nearest integer
    5. It does this for each step

    Args:
        black (tuple): The first color
        random_color (tuple): The second color
        interval (int): The number of steps to take between the two colors"""

    derandom_color = [(t - f) / interval for f, t in zip(random_color2, random_color)]
    for i in range(interval):
        yield [round(t + det * i) for t, det in zip(random_color2, derandom_color)]


def export_util(c, type: str):    # sourcery skip: low-code-quality
    """
    Exports the words from the database to a flashcard image

    Args:
        c (sqlite3.Cursor): The cursor object
        type (str): The type of words to be exported
    """

    if not (rows := c.fetchall()):
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable=f"No words found for selected criteria: {type}",
            )
        )

    # Create a new image with a white background
    width, height = 1080, 1080

    my_colors = [
        # shades of red
        (255, 99, 71),
        (255, 127, 80),
        (205, 92, 92),
        (240, 128, 128),
        (233, 150, 122),
        (250, 128, 114),
        (255, 160, 122),
        # shades of green
        (50, 205, 50),
        (144, 238, 144),
        (152, 251, 152),
        (143, 188, 143),
        (0, 250, 154),
        (0, 255, 127),
        # shades of blue
        (0, 255, 255),
        (224, 255, 255),
        (0, 206, 209),
        (64, 224, 208),
        (72, 209, 204),
        (175, 238, 238),
        (127, 255, 212),
        (176, 224, 230),
        (95, 158, 160),
        (70, 130, 180),
        (100, 149, 237),
        (0, 191, 255),
        (30, 144, 255),
        # shades of purple
        (106, 90, 205),
        (123, 104, 238),
        (147, 112, 219),
        (153, 50, 204),
        (186, 85, 211),
        (128, 0, 128),
        (216, 191, 216),
        (221, 160, 221),
        (238, 130, 238),
        (255, 0, 255),
        # shades of pink
        (199, 21, 133),
        (219, 112, 147),
        (255, 20, 147),
        (255, 105, 180),
        (255, 182, 193),
        (255, 192, 203),
    ]

    # ----------------- Progress Bar -----------------#

    for row, _ in zip(
        rows, track(range(len(rows) - 1), description=" 🔃 Exporting Flashcards ")
    ):
        # ----------------- Progress Bar -----------------#

        tag = row[1] if type == "tag" else None
        word = row[0]
        image = Image.new("RGB", (width, height), "white")

        # Get a drawing context
        draw = ImageDraw.Draw(image)

        black = (0, 0, 0)
        random_color = random.choice(my_colors)
        random_color2 = random.choice(my_colors) 

        if random_color == random_color2:
            random_color2 = random.choice(my_colors)

        # print(random_color)
        for i, color in enumerate(interpolate(random_color, random_color2, image.width * 2)):
            draw.line([(i, 0), (0, i)], tuple(color), width=1)

        # Use ImageFont to specify the font and size of the text
        font = ImageFont.truetype("../assets/FTLTLT.ttf", 36)
        headingfont = ImageFont.truetype("../assets/FTLTLT.ttf", 64)

        # draw the watermark in the top right corner
        watermark = Image.open("../assets/VocabCLI -  White.png")
        watermark = watermark.resize((200, 200))
        image.paste(watermark, (880, -50), mask=watermark)

        # Draw the word and its definition on the image
        draw.text(
            (50, 50),
            word.upper(),
            fill="white",
            font=headingfont,
            stroke_width=2,
            stroke_fill="black",
        )

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

            text_size = draw.textsize(tag, font=font)
            # calculate the position of the text to center it on the image
            x = 150
            y = 150

            # add some padding
            padding = 15
            box = (x - padding, y - padding, x + text_size[0] + padding, y + text_size[1] + padding)

            # draw the background
            draw.rectangle(box, fill="white")

            draw.text((150, 150), tag, fill="black", font=font)

        # get the dictionary of definitions:examples
        def_and_example = flashcard_definition(word)

        for count, (definition, example) in enumerate(def_and_example.items(), start=1):
            definition = textwrap.fill(definition, width=65)
            y_pos = 150 + (count * 200)

            # if the definition has an example, add it to the flashcard
            if example:
                example = textwrap.fill(example, width=65)
                draw.text(
                    (50, y_pos),
                    f"{count}. {definition}\n eg. {example}",
                    fill="black",
                    font=font,
                )
            else:
                draw.text(
                    (50, y_pos), f"{count}. {definition}", fill="black", font=font
                )

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


def generate_all_flashcards():
    """Generate flashcards for all words in the database"""

    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words")
    export_util(c, type="all words")


def generate_mastered_flashcards():
    """Generate flashcards for all mastered words in the database"""

    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words WHERE mastered=1")
    export_util(c, type="mastered")


def generate_learning_flashcards():
    """Generate flashcards for all learning words in the database"""

    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words WHERE learning=1")
    export_util(c, type="learning")


def generate_favorite_flashcards():
    """Generate flashcards for all favorite words in the database"""

    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT(word) FROM words WHERE favorite=1")
    export_util(c, type="favorite")


def generate_tag_flashcards(query: str):
    """
    Generate flashcards for all words with a specific tag in the database

    Args:
        query (str): the tag to search for
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT(word), tag FROM words WHERE tag=?", (query,))
    export_util(c, type="tag")


# def export_word(query: str):
#     conn = createConnection()
#     c = conn.cursor()
#     c.execute("SELECT DISTINCT(word) FROM words WHERE word=?", (query,))
#     export_util(c, type="word")

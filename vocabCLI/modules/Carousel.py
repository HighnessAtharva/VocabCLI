import glob
from tkinter import *
from PIL import ImageTk, Image
from Graph import *
import typer
import os


def show_slider() -> None:
    """ 
    1. Sets up the GUI window
    2. Dumps the images to the folder
    3. Deletes the images if already existing
    4. Sets up the images
    5. Creates a global counter variable 
    """
    # set up the tkinter window
    root = Tk()
    root.title("VocabCLI Graphs")
    root.geometry("1200x700")
    root.iconbitmap("../assets/logos/VocabCLI.ico")

    # dump all the images to the folder
    viz_learning_vs_mastered(popup=False)
    viz_top_tags_bar(popup=False)
    viz_top_tags_pie(popup=False)
    viz_top_words_bar(popup=False)
    viz_top_words_pie(popup=False)
    viz_word_distribution_month(popup=False)
    viz_word_distribution_week(popup=False)
    viz_word_distribution_year(popup=False)
    viz_word_distribution_category(popup=False)

    # delete the images if already existing
    images_to_delete = glob.glob("../exports/GRAPH-*.png")
    for image in images_to_delete:
        # check if file eixsts or not
        if os.path.exists(image):
            os.remove(image)

    # set up the images
    image1 = ImageTk.PhotoImage(Image.open(
        "exports/GRAPH-learning_vs_mastered.png").resize((1200, 700)))
    image2 = ImageTk.PhotoImage(Image.open(
        "exports/GRAPH-top_tags_bar.png").resize((1200, 700)))
    image3 = ImageTk.PhotoImage(Image.open(
        "exports/GRAPH-top_words_bar.png").resize((1200, 700)))
    image4 = ImageTk.PhotoImage(Image.open(
        "exports/GRAPH-word_distribution_month.png").resize((1200, 700)))
    image5 = ImageTk.PhotoImage(Image.open(
        "exports/GRAPH-words_distribution_week.png").resize((1200, 700)))
    image6 = ImageTk.PhotoImage(Image.open(
        "exports/GRAPH-top_tags_pie.png").resize((1200, 700)))
    image7 = ImageTk.PhotoImage(Image.open(
        "exports/GRAPH-top_words_pie.png").resize((1200, 700)))
    image8 = ImageTk.PhotoImage(Image.open(
        "exports/GRAPH-word_distribution_category.png").resize((1200, 700)))
    image_list = [image1, image2, image3,
                  image4, image5, image6, image7, image8]

    global counter
    counter = 0

    def ChangeImage():
        """ 
        1. Changes the image
        2. Changes the info label
        """
        global counter
        if counter < len(image_list) - 1:
            counter += 1
        else:
            counter = 0
        imageLabel.config(image=image_list[counter])
        infoLabel.config(text=f"Image {str(counter + 1)} of {len(image_list)}")
    
    # set up the components
    imageLabel = Label(root, image=image1)
    infoLabel = Label(
        root, text=f"Image 1 of {len(image_list)}", font="Helvetica, 20")
    button = Button(root, text="Change", width=20, height=2,
                    bg="purple", fg="white", command=ChangeImage)
    
    # display the components
    imageLabel.pack()
    infoLabel.pack()
    button.pack(side="bottom", pady=3)
    
    # run the main loop
    root.mainloop()

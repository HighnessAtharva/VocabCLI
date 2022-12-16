import glob
from tkinter import *
from PIL import ImageTk, Image
from Graph import *
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
 
# set up the images
image1 = ImageTk.PhotoImage(Image.open("exports/GRAPH-learning_vs_mastered.png").resize((1200, 700)))
image2 = ImageTk.PhotoImage(Image.open("exports/GRAPH-top_tags_bar.png").resize((1200, 700)))
image3 = ImageTk.PhotoImage(Image.open("exports/GRAPH-top_words_bar.png").resize((1200, 700)))
image4 = ImageTk.PhotoImage(Image.open("exports/GRAPH-word_distribution_month.png").resize((1200, 700)))
image5 = ImageTk.PhotoImage(Image.open("exports/GRAPH-words_distribution_week.png").resize((1200, 700)))
image_list = [image1, image2, image3, image4, image5]
counter = 0

def ChangeImage():
    global counter
    if counter < len(image_list) - 1:
        counter += 1
    else:
        counter = 0
    imageLabel.config(image=image_list[counter])
    infoLabel.config(text=f"Image {str(counter + 1)} of {len(image_list)}")
# set up the components
imageLabel = Label(root, image=image1)
infoLabel = Label(root, text="Image 1 of 5", font="Helvetica, 20")
button = Button(root, text="Change", width=20, height=2, bg="purple", fg="white", command=ChangeImage)
# display the components
imageLabel.pack()
infoLabel.pack()
button.pack(side="bottom", pady=3)
# run the main loop
root.mainloop()


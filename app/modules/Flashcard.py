import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import PIL.ImageTk


# draw an image with the text hello world
base = PIL.Image.new('RGB', (100, 100), (255, 255, 255))
draw = PIL.ImageDraw.Draw(base)
draw.text((0, 0), "hello world", (0, 0, 0))

# change image dimensions to 200x200
base = base.resize((200, 200))
base.save('hello_world.png')


# create a new image with the text "hello world"

# save it to the dis

import re
import tkinter as tk
from PIL import Image, ImageTk, PngImagePlugin
import time

LM_USE_SVG = 0
try:
   from cairosvg import svg2png
   LM_USE_SVG = 1
except:
   print("WARNING: Unable to import cairosvg. No svg images will be displayed.")
   LM_USE_SVG = 0

# graphical classes and functions
print("Loading graphics...")

def photoimage_from_svg(filename = "",size = "48"):
   # this one works, but does not allow me to set the size.
   # this is kept as an example of how to open a svg without saving to a file.
   # open svg
   item = svg2png(url=filename, parent_width = size, parent_height = size)
   return ImageTk.PhotoImage(data=item)

def empty_photoimage(size=24):
   photo = Image.new("RGBA",[size,size])
   return ImageTk.PhotoImage(image=photo)

def image_from_svg(filename = "",size = 0):
   # open svg
   if LM_USE_SVG == 1:
      if size == 0:
         # unscaled
         svg2png(url=filename,write_to="/tmp/example_temp_image.png")
      else:
         svg2png(url=filename,write_to="/tmp/example_temp_image.png",parent_width = size,parent_height = size)
      photo = Image.open("/tmp/example_temp_image.png")
   else:
      photo = Image.new("RGBA",[size,size])
   return photo

def get_scaled_icon(iconfilename, size = 0):

   try:
      print("Opening icon file",iconfilename)
      # try an svg
      if re.compile(".*\.svg").match(iconfilename):
         photo = image_from_svg(filename=iconfilename, size=size)
      else:
         photo = Image.open(iconfilename)
   except Exception as f:
      print("Error with icon file:", f)
      return empty_photoimage()

   if size != 0 and (type(photo) is Image or type(photo) is PngImagePlugin.PngImageFile):
      photo.thumbnail(size=[size, size])

   if not type(photo) is ImageTk.PhotoImage:
      try:
         photo = ImageTk.PhotoImage(photo)
      except Exception as e:
         print("Error was ",e)
   return photo

class App:
    def __init__(self, master, image_path):
        # self.frame = tk.Frame(master)
        # self.frame.grid(row=0)
        self.frame = tk.Frame(master)
        self.image_path = image_path

        print("image_path", image_path)
        image = get_scaled_icon(image_path, 512)
        # self.button1 = tk.Button(self.frame, text="Scaled to 24x24", image=image, compound=tk.LEFT)
        # self.button1.grid(row=0,column=0)
        self.image = tk.Image(self.frame, text="Scaled to 24x24", image=image, compound=tk.LEFT)
        self.image.pack()

    def quitaction(self,b=None):
        print("Closing the window...")
        root.destroy()
   
    def updateImage(self, image_path):
        image = get_scaled_icon(image_path, 512)
        print("image_path", image_path)
        self.image = tk.Button(self.frame, text="Scaled to 24x24", image=image, compound=tk.LEFT)
        self.image.pack()

# root = tk.Tk()
# LABEL = tk.Label(ROOT, text="Hello, world!")
# LABEL.pack()
LOOP_ACTIVE = True
root = tk.Tk()
root.title("Chess UI")
app = App(root, "./hello.svg")
while LOOP_ACTIVE:
    root.update()
    USER_INPUT = input("Give me your command! Just type \"exit\" to close: ")
    if USER_INPUT == "exit":
        root.quit()
        LOOP_ACTIVE = False
    else:
        # LABEL = Label(ROOT, text=USER_INPUT)
        # LABEL.pack()
        app.updateImage(USER_INPUT)
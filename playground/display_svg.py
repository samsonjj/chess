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
      self.frame = tk.Frame(master)
      self.frame.grid(row=0)

      self.image_path = image_path

      image = get_scaled_icon(image_path, 512)
      self.button1 = tk.Button(self.frame, text="Scaled to 24x24", image=image, compound=tk.LEFT)
      self.button1.grid(row=0,column=0)

   def quitaction(self,b=None):
      print("Closing the window...")
      root.destroy()
   
   def updateImage(self):
      image = get_scaled_icon(image_path, 512)
      self.button2 = tk.Button(self.frame, text="Scaled to 24x24", image=image, compound=tk.LEFT)
      self.button2.grid(row=0,column=0)


# MAIN LOOP
def init(cb, image_path):
   root = tk.Tk()
   root.title("Chess UI")
   imgicon = get_scaled_icon(image_path, 512)
   root.tk.call('wm','iconphoto', root._w, imgicon)
   app = App(root, image_path)

   def my_loop():
      cb()
      app.updateImage()
   
   root.after(0, lambda: app.updateImage())
   root.mainloop()

if __name__ == "__main__":
   init(lambda: print('hello'), "./hello.svg")
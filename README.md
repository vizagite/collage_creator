<head>
  <meta property="og:title" content="Bookcovers collage creator">
  <meta property="og:description" content="Works on all systems with python">
</head>

# Image Collage Creator

![my 2025 book collage](collage_output.jpg)

I wanted to create bookcover collages like this to share with my friends.
This Python script helps you create same beautiful collages from your images. It's simple to use and works with common image formats like JPG, PNG, and more.

## Requirements

- Python 3 installed on your computer.
- `Pillow` library (for image processing). The script will guide you to install it if needed.

## How to Use
1. **Prepare Your Images**

   Keep all images from which you want to make collage in a single new folder. nothing else in that folder.

2. **Save the Script**  
   
   Now save [this script](https://github.com/vizagite/collage_creator/blob/main/collage_gen.py?raw=true) and move it into the above folder of images. `ctrl+s` shortcut.

3. **Open a Terminal or Command Prompt** 
    
    In the same folder, you can open a terminal or command prompt window.
    or open command prompt and Navigate to our folder containing `collage_gen.py`. use the commands like `cd` or `chdir` to navigate.

4. **Run the Script**  
   
   Use the following commands now to create a collage:

   `python collage_gen.py` or `python collage_gen.py -c 7` to adjust columns

   **TIP**: Rename the images as 01, 02, ... in order for deciding the order in final collage. Make sure to not disturb the file extensions part while renaming (file extensions are .jpg, .png, ...)

5. **For more advanced usage pass other options**
    
    `python collage_gen.py --columns 3 --input-dir "my_images" --output "my_collage.jpg" --width 400 --height 600 --padding 15 --background "black"`

Enjoy creating your collages! 🎉


## Troubleshooting
- If you see an error about Pillow not being installed, type y when prompted to install it.
- Make sure your images are in the correct folder and have the right file extensions.
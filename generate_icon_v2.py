from PIL import Image, ImageDraw
import os

def generate_ico():
    # We create the largest first and let Pillow handle the sizes
    # or follow the user's manual list if they prefer custom drawing per size
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    for size in sizes:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Body gembok (using user's logic)
        margin = size // 8
        draw.rounded_rectangle([margin, size//2, size-margin, size-margin],
                               radius=size//10, fill=(130, 80, 200, 255))
        # Shackle
        sw = size // 6
        draw.arc([size//4, margin, size*3//4, size//2+size//8],
                 start=180, end=0, fill=(80, 80, 120, 255), width=sw)
        # Keyhole
        cx, cy = size//2, size*3//4
        r = size//10
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 255, 255, 200))
        images.append(img)
    
    # Save using the largest image as the base and include others
    # Pillow's ICO writer is a bit specific. 
    # The best way is to provide the list of images to images[0].save
    images[0].save('icon.ico', format='ICO', sizes=[(s,s) for s in sizes],
                   append_images=images[1:])
    print('icon.ico generated successfully!')

if __name__ == "__main__":
    generate_ico()

from PIL import Image, ImageDraw
import os

def generate_lock_icon():
    # Size 256x256 for high quality ICO
    size = (256, 256)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Colors (Match app theme)
    purple_accent = (189, 147, 249, 255) # #bd93f9
    blue_grey = (98, 114, 164, 255)     # #6272a4 (shackle)
    dark_bg = (40, 42, 54, 255)         # #282a36 (body background)
    white = (248, 248, 242, 255)        # #f8f8f2 (text/detail color)

    # 1. Draw the shackle (Upper part)
    # [left, top, right, bottom]
    shackle_bbox = [60, 30, 196, 170]
    draw.arc(shackle_bbox, start=180, end=0, fill=blue_grey, width=35)
    
    # Draw vertical poles for the shackle
    draw.rectangle([60, 100, 95, 160], fill=blue_grey)
    draw.rectangle([161, 100, 196, 160], fill=blue_grey)

    # 2. Draw the main body (Rounded rectangle)
    # [left, top, right, bottom] - overlap the poles
    body_bbox = [40, 120, 216, 230]
    draw.rounded_rectangle(body_bbox, radius=25, fill=purple_accent)
    
    # Inner body detail (like a shaded area)
    inner_bbox = [60, 140, 196, 210]
    draw.rounded_rectangle(inner_bbox, radius=15, fill=dark_bg)

    # 3. Draw keyhole
    # Circle for head of keyhole
    draw.ellipse([113, 155, 143, 185], fill=white)
    # Triangle/Rectangle for bottom of keyhole
    draw.polygon([(128, 170), (120, 205), (136, 205)], fill=white)

    # Save PNG (for base64) & ICO (for EXE)
    image.save("icon.png")
    # ICO often needs multiple sizes (16, 32, 48, 256)
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    image.save("icon.ico", sizes=icon_sizes)
    
    print("Icons generated successfully: icon.png and icon.ico")

if __name__ == "__main__":
    generate_lock_icon()

from PIL import Image, ImageDraw, ImageFont

def apply_text_overlay(img, headline, layout):
    """
    Accepts a PIL Image object directly and returns the modified Image.
    """
    img = img.convert("RGBA")
    width, height = img.size
    draw = ImageDraw.Draw(img)

    # Scale font size to image width (approx 6% of width)
    # Note: For production, you'd bundle a .ttf font file
    try:
        font = ImageFont.truetype("arial.ttf", size=int(width * 0.06))
    except:
        font = ImageFont.load_default()

    # Calculate text position
    text_bbox = draw.textbbox((0, 0), headline, font=font)
    tw, th = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    
    margin = int(layout.get("safe_margin_ratio", 0.1) * height)
    x = (width - tw) // 2
    
    pos = layout.get("text_position", "bottom_center")
    if pos == "top_center": y = margin
    elif pos == "center": y = (height - th) // 2
    else: y = height - th - margin

    # Draw background box
    if layout.get("background_style") != "none":
        draw.rectangle([x-10, y-10, x+tw+10, y+th+10], fill=(0,0,0,140))

    draw.text((x, y), headline, fill=layout.get("text_color", "white"), font=font)
    return img
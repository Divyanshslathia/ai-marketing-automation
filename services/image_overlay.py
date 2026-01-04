from PIL import Image, ImageDraw, ImageFont


def apply_text_overlay(
    image_path: str,
    output_path: str,
    headline: str,
    layout: dict,
):
    """
    Applies headline text to an image using layout rules.
    """

    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    draw = ImageDraw.Draw(img)

    # --- Font setup ---
    font_size = int(width * 0.08)
    font = ImageFont.load_default()

    # --- Measure text ---
    text_bbox = draw.textbbox((0, 0), headline, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    margin = int(layout["safe_margin_ratio"] * height)

    # --- Position calculation ---
    if layout["text_position"] == "top_center":
        x = (width - text_width) // 2
        y = margin
    elif layout["text_position"] == "center":
        x = (width - text_width) // 2
        y = (height - text_height) // 2
    else:  # bottom_center
        x = (width - text_width) // 2
        y = height - text_height - margin

    # --- Background strip ---
    if layout["background_style"] != "none":
        padding = 20
        rect_coords = [
            x - padding,
            y - padding,
            x + text_width + padding,
            y + text_height + padding,
        ]
        draw.rectangle(rect_coords, fill=(0, 0, 0, 160))

    # --- Draw text ---
    draw.text(
        (x, y),
        headline,
        fill=layout["text_color"],
        font=font,
    )

    img.save(output_path)

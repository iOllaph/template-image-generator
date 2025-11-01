import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Constants for project structure
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"
FONTS_DIR = "fonts"

def generate_image(template_file, title, subtitle):
    # Build full paths
    template_path = os.path.join(TEMPLATE_DIR, template_file)
    title_font_path = os.path.join(FONTS_DIR, "Jost-Bold.ttf")
    subtitle_font_path = os.path.join(FONTS_DIR, "Jost-ExtraLight.ttf")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Create output filename with current datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output_{timestamp}.png"
    output_path = os.path.join(OUTPUT_DIR, output_file)

    # Load image and drawing context
    image = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    # Load fonts
    title_font = ImageFont.truetype(title_font_path, 80)
    subtitle_font = ImageFont.truetype(subtitle_font_path, 40)

    width, height = image.size

    # Title size
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]

    # Subtitle size
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_height = subtitle_bbox[3] - subtitle_bbox[1]

    # Extra spacing (40% of title height)
    extra_spacing = title_height * 0.4

    # Total block height for vertical centering
    total_height = title_height + extra_spacing + subtitle_height
    top_y = (height - total_height) / 2

    # Text positions
    title_position = ((width - title_width) / 2, top_y)
    subtitle_position = ((width - subtitle_width) / 2, top_y + title_height + extra_spacing)

    # Draw text
    draw.text(title_position, title, font=title_font, fill="black")
    draw.text(subtitle_position, subtitle, font=subtitle_font, fill="black")

    # Save output
    image.save(output_path)
    print(f"Image saved to {output_path}")


# Example usage
if __name__ == "__main__":
    generate_image(
        template_file="template.png",
        title="PABLLO CARVALHO",
        subtitle="Professor - 3° AO 6° ANO (9-12)"
    )

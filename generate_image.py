import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import os

# Constants
TEMPLATE_DIR = "templates"
FONTS_DIR = "fonts"

app = FastAPI(title="Image Generator API")

# Request body model
class ImageRequest(BaseModel):
    title: str
    subtitle: str

def generate_image_bytes(title: str, subtitle: str, template_file="template.png"):
    # Paths
    template_path = os.path.join(TEMPLATE_DIR, template_file)
    title_font_path = os.path.join(FONTS_DIR, "Jost-Bold.ttf")
    subtitle_font_path = os.path.join(FONTS_DIR, "Jost-ExtraLight.ttf")

    # Load template
    image = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Load fonts
    title_font = ImageFont.truetype(title_font_path, 80)
    subtitle_font = ImageFont.truetype(subtitle_font_path, 40)

    # Title and subtitle sizes
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)

    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_height = subtitle_bbox[3] - subtitle_bbox[1]

    # Spacing and centering
    extra_spacing = title_height * 0.4
    total_height = title_height + extra_spacing + subtitle_height
    top_y = (height - total_height) / 2

    title_position = ((width - title_width) / 2, top_y)
    subtitle_position = ((width - subtitle_width) / 2, top_y + title_height + extra_spacing)

    # Draw text
    draw.text(title_position, title, font=title_font, fill="black")
    draw.text(subtitle_position, subtitle, font=subtitle_font, fill="black")

    # Save to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes

# POST endpoint
@app.post("/generate")
def generate_image(request: ImageRequest):
    try:
        img_bytes = generate_image_bytes(request.title, request.subtitle)
        return StreamingResponse(img_bytes, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

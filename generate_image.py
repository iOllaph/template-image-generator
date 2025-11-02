import base64
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import secrets
import io
from PIL import Image, ImageDraw, ImageFont
import os

# Setup (as before)
TEMPLATE_DIR = "templates"
FONTS_DIR = "fonts"
app = FastAPI()
security = HTTPBasic()
USERNAME = os.getenv("API_USERNAME", "admin")
PASSWORD = os.getenv("API_PASSWORD", "mypassword")

class ImageRequest(BaseModel):
    title: str
    subtitle: str

def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

def generate_image_bytes(title: str, subtitle: str, template_file="template.png"):
    template_path = os.path.join(TEMPLATE_DIR, template_file)
    title_font_path = os.path.join(FONTS_DIR, "Jost-Bold.ttf")
    subtitle_font_path = os.path.join(FONTS_DIR, "Jost-ExtraLight.ttf")

    image = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    title_font = ImageFont.truetype(title_font_path, 80)
    subtitle_font = ImageFont.truetype(subtitle_font_path, 40)

    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)

    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_height = subtitle_bbox[3] - subtitle_bbox[1]

    extra_spacing = title_height * 0.4
    total_height = title_height + extra_spacing + subtitle_height
    top_y = (height - total_height) / 2

    title_position = ((width - title_width) / 2, top_y)
    subtitle_position = ((width - subtitle_width) / 2, top_y + title_height + extra_spacing)

    draw.text(title_position, title, font=title_font, fill="black")
    draw.text(subtitle_position, subtitle, font=subtitle_font, fill="black")

    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes

@app.post("/generate")
def generate_image(request: ImageRequest, authorized: bool = Depends(check_auth)):
    try:
        img_bytes = generate_image_bytes(request.title, request.subtitle)
        # convert to Base64
        base64_str = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
        return {
            "bytes": list(img_bytes.getvalue()),  # optional raw bytes as list
            "base64": base64_str
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

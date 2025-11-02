# Template Image Generator API

A lightweight FastAPI project to generate images from a template with dynamic titles and subtitles. Supports **HTTP Basic Auth** and can be run locally or via Docker.

---

## Features

- Add dynamic **title** and **subtitle** text
- Centered text with automatic spacing
- Simple authentication via username/password
- Ready to run with Docker

---

## Folder Structure

```

image-generator/
├── fonts/             # TTF font files
│   ├── Jost-Bold.ttf
│   └── Jost-ExtraLight.ttf
├── templates/         # Template image
│   └── template.png
├── output/            # Generated images (ignored in Git)
├── generate_image.py             # FastAPI application
├── Dockerfile
├── requirements.txt
└── README.md

````

---

## Local Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/template-image-generator.git
cd template-image-generator
````

2. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
# OR
venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the API**

```bash
uvicorn generate_image:app --reload
```

* API will be available at: `http://127.0.0.1:8000`
* Swagger UI: `http://127.0.0.1:8000/docs`

---

## API Usage

### POST `/generate`

Send a JSON request body with `title` and `subtitle`. Requires **HTTP Basic Auth**.

**Request Example (curl):**

```bash
curl -u admin:mypassword -X POST "http://127.0.0.1:8000/generate" \
-H "Content-Type: application/json" \
-d '{"title":"PABLLO CARVALHO","subtitle":"Professor - 3° AO 6° ANO (9-12)"}' \
--output output.png
```

**Response Example (JSON)**

```json
{
  "bytes": [137, 80, 78, 71, ...],
  "base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

* `base64` — The generated PNG image encoded as a Base64 string.
* `bytes` — (Optional) Raw image bytes as a numeric array.

---

**Request Body (JSON)**

```json
{
  "title": "Your Title",
  "subtitle": "Your Subtitle"
}
```

---

## Authentication

* Simple **HTTP Basic Auth**.
* Default credentials (can be overridden in Docker or environment variables):

```bash
USERNAME=admin
PASSWORD=mypassword
```

---

## Docker Setup

1. **Build the image**

```bash
docker build -t image-generator-api .
```

2. **Run the container with custom credentials**

```bash
docker run -d -p 8000:8000 \
-e API_USERNAME=myuser \
-e API_PASSWORD=mypassword \
image-generator-api
```

3. **Access the API**

```
http://localhost:8000/generate
```

---

## Notes

* Place all fonts in `fonts/` and templates in `templates/`.
* `output/` is ignored in Git; generated images are saved there only if running locally.
* For production, always set **secure passwords** via environment variables.

---

## License

MIT License


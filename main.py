from fastapi import FastAPI
import io
import logging
from svglib.svglib import svg2rlg
from reportlab.graphics.renderPM import drawToPIL
from starlette.responses import StreamingResponse

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Hello from Vercel"}


@app.get("/svg")
async def generate_svg():
    logger.info("Generating SVG")
    try:
        svg = """
        <svg height="140" width="500" xmlns="http://www.w3.org/2000/svg">
            <ellipse cx="120" cy="80" rx="100" ry="50" 
            style="fill:yellow;stroke:green;stroke-width:3" />
        </svg>
        """

        # Convert SVG to PNG using svglib and Pillow
        drawing = svg2rlg(io.BytesIO(svg.encode()))
        img = drawToPIL(drawing)

        # Save to a BytesIO buffer
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        return StreamingResponse(img_buffer, media_type="image/png")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return {"error": "Failed to generate PNG"}


# Vercel ASGI handler
from mangum import Mangum

handler = Mangum(app)

from fastapi import FastAPI
import io
import logging
import cairosvg
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
        png_bytes = cairosvg.svg2png(bytestring=svg.encode('utf-8'))
        return StreamingResponse(io.BytesIO(png_bytes), media_type="image/png")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return {"error": "Failed to generate PNG"}

# Vercel ASGI handler
from mangum import Mangum
handler = Mangum(app)

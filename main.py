from fastapi import FastAPI
import cairo
import io
import logging
from starlette.responses import StreamingResponse

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler('app.log')  # Log to file
    ]
)

# Create a logger instance
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def say_hello():
    logger.info(f"succes")
    return {"message": f"Hello"}

@app.get("/svg")
async def root():
    logger.debug("Starting root endpoint processing")
    try:
        svg = """
        <svg height="140" width="500" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="120" cy="80" rx="100" ry="50" style="fill:yellow;stroke:green;stroke-width:3" />
      Sorry, your browser does not support inline SVG.  
    </svg>
        """

        logger.info("Writing SVG to file")
        with open("/tmp/test.svg", "w") as f:
            f.write(svg)
            surface = cairo.SVGSurface("/tmp/test.svg", 500, 140)
            surface.write_to_png("/tmp/test.png")
            logger.debug("PNG file created successfully")

            with open("/tmp/test.png", "rb") as f:
                image_stream = io.BytesIO(f.read())
                logger.info("Image stream created successfully")
                return StreamingResponse(image_stream, media_type="image/png")
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}", exc_info=True)
        raise


@app.get("/hello/{name}")
async def say_hello(name: str):
    logger.info(f"Saying hello to {name}")
    return {"message": f"Hello {name}"}


# Add startup and shutdown event handlers
@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")

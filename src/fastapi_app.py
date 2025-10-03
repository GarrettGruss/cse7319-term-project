from fastapi import FastAPI
import dotenv
from src.controller.post_controller import PostController

# Load environment variables from .env file
dotenv.load_dotenv()

app = FastAPI()
controller = PostController()


@app.get("/generate-post")
async def generate_post():
    """Generate a random Reddit post with LLM response"""
    return controller.get_random_post_with_llm_response()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

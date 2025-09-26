from fastapi import FastAPI
from src.controller.post_controller import PostController

app = FastAPI()
controller = PostController()

@app.get("/generate-post")
async def generate_post():
    """Generate a random Reddit post with LLM response"""
    return controller.get_random_post_with_llm_response()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
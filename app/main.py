from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World!"}


@app.get("/search")
async def search_library() -> dict[str, str]:
    return {"message": "Search Complete!"}

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

BASE_DIR = Path(__file__).parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


posts: list[dict] = [
    {
        "id": 1,
        "author": "Jason Bourne",
        "title": "FastAPI is cool",
        "content": "I'm learning how to use this framework for my interview.",
        "date_posted": "November 5, 2026",
    },
    {
        "id": 2,
        "author": "Michelle Obama",
        "title": "I love Python",
        "content": "Python is a great programming language and extremely versatile.",
        "date_posted": "November 8, 2026",
    },
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )


@app.get("/api/posts")
def get_posts():
    return posts

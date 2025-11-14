import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
<<<<<<< Updated upstream
from backend.routers.database import init_db
from backend.routers import lessons
=======
from backend.database import init_db
from lessons import *
>>>>>>> Stashed changes

import uvicorn

app = FastAPI()

init_db()


<<<<<<< Updated upstream
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend", "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend"))

=======

app.mount("/static", StaticFiles(directory=os.path.join("frontend", "static")), name="static")
>>>>>>> Stashed changes

templates = Jinja2Templates(directory=os.path.join("frontend"))
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    logged_in = request.cookies.get("logged_in") == "true"
    return templates.TemplateResponse("index.html", {"request": request, "logged_in": logged_in})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "1234":
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="logged_in", value="true")
        return response
    return {"error": "Username yoki password xato"}

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="logged_in")
    return response

# 🔹 Main page endpoint
@app.get("/main", response_class=HTMLResponse)
def main_page(request: Request):
    logged_in = request.cookies.get("logged_in") == "true"
    return templates.TemplateResponse("main.html", {"request": request, "logged_in": logged_in})

# 🔹 Lessons page endpoint
@app.get("/lessons-page", response_class=HTMLResponse)
def lessons_page(request: Request):
    logged_in = request.cookies.get("logged_in") == "true"
    return templates.TemplateResponse("lessons.html", {"request": request, "logged_in": logged_in})



def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_server()

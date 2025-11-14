import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers.database import init_db
from routers import lessons

import uvicorn

app = FastAPI()

init_db()

# Routerni ulash
app.include_router(lessons.router)

# Frontend papka yo'lini tuzatish
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")

# Static fayllar (CSS, JS)
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Templates (HTML fayllar)
templates = Jinja2Templates(directory=frontend_path)

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
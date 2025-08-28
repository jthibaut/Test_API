from fastapi import FastAPI
from app.routes import cleaning
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(cleaning.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de nettoyage de données"}

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request, data: str = Form(...)):
    result = f"Tu as envoyé : {data}"
    return templates.TemplateResponse("form.html", {"request": request, "result": result})

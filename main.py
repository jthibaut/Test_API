from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from io import BytesIO
from uuid import uuid4
from app.cleaning import clean_dataframe

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Stockage temporaire des CSV par upload (UUID → bytes)
uploaded_csvs = {}

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    """Affiche le formulaire HTML."""
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def handle_upload(request: Request, file: UploadFile = File(...)):
    """
    Traite le CSV uploadé :
    - Nettoyage via cleaning.py
    - Affichage limité aux 20 premières lignes
    - Remplacement des CSV temporaires existants
    """
    # --- Reset temporaire ---
    uploaded_csvs.clear()  # supprime tous les anciens CSV pour éviter conflit

    # Lecture du CSV
    contents = await file.read()
    df = pd.read_csv(BytesIO(contents))

    # Nettoyage
    cleaned_df = clean_dataframe(df)

    # Conversion en HTML pour affichage limité
    cleaned_html = cleaned_df.head(20).to_html(classes="table table-striped", index=False)

    # Générer un UUID unique pour le téléchargement
    file_id = str(uuid4())
    stream = BytesIO()
    cleaned_df.to_csv(stream, index=False)
    stream.seek(0)
    uploaded_csvs[file_id] = stream.getvalue()

    return templates.TemplateResponse("upload.html", {
        "request": request,
        "filename": file.filename,
        "table": cleaned_html,
        "file_id": file_id
    })

@app.get("/download/{file_id}", response_class=StreamingResponse)
async def download_csv(file_id: str):
    """Téléchargement du CSV nettoyé."""
    if file_id not in uploaded_csvs:
        return {"error": "Fichier introuvable ou expiré."}

    stream = BytesIO(uploaded_csvs[file_id])
    stream.seek(0)
    return StreamingResponse(
        stream,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=cleaned_data.csv"}
    )

@app.get("/", response_class=HTMLResponse)
async def redirect_to_upload(request: Request):
    """Redirection vers /upload."""
    return templates.TemplateResponse("upload.html", {"request": request})

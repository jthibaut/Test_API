from fastapi import FastAPI, File, UploadFile
import pandas as pd
from sklearn.preprocessing import StandardScaler
from io import BytesIO

app = FastAPI()

@app.post("/clean")
async def clean_data(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(BytesIO(contents))

    # Nettoyage
    df.drop_duplicates(inplace=True)
    df.fillna(df.mean(numeric_only=True), inplace=True)

    # Normalisation
    num_cols = df.select_dtypes(include='number').columns
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])

    # Retourner le fichier nettoyé
    return df.to_json(orient="records")

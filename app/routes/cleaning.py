# app/cleaning.py
import pandas as pd
from sklearn.preprocessing import StandardScaler

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie un DataFrame Pandas :
    1. Supprime les doublons
    2. Remplace les NaN numériques par la moyenne
    3. Normalise les colonnes numériques
    """
    df = df.copy()

    # Nettoyage
    df.drop_duplicates(inplace=True)
    df.fillna(df.mean(numeric_only=True), inplace=True)

    # Normalisation
    num_cols = df.select_dtypes(include='number').columns
    if not df[num_cols].empty:
        scaler = StandardScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])

    return df

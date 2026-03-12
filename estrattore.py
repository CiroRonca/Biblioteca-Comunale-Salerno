import pandas as pd
import json

def converti_excel_in_json(file_excel, file_json):
    print("Sto leggendo il tuo file Excel perfetto...")
    
    # 1. Leggiamo l'Excel con Pandas (usando read_excel al posto di read_csv)
    try:
        df = pd.read_excel(file_excel)
    except FileNotFoundError:
        print(f"Errore: Non trovo il file '{file_excel}'. Assicurati che sia nella stessa cartella!")
        return
    except ImportError:
        print("Errore: Manca la libreria per leggere i file Excel. Scrivi nel terminale: pip install openpyxl")
        return

    catalogo_json = []
    
    # Colori per dare un bell'effetto grafico alternato alle schede del tuo sito
    colori = ["#1B3A5C", "#2E6DA4", "#C4622D", "#E8A838", "#3A6B4A", "#6B4C3B"]

    # 2. Scorriamo ogni riga del foglio Excel
    for index, row in df.iterrows():
        # Prendiamo i dati, se una cella è vuota (NaN) ci mettiamo "N/D"
        titolo = str(row['Titolo']) if pd.notna(row.get('Titolo')) else "N/D"
        autore = str(row['Autore']) if pd.notna(row.get('Autore')) else "N/D"
        pagine = str(row['Pagine']) if pd.notna(row.get('Pagine')) else "N/D"
        codice = str(row['Codice']) if pd.notna(row.get('Codice')) else "N/D"
        
        # Piccola pulizia extra
        titolo = titolo.replace('Scansionato con CamScanner', '').strip()
        autore = autore.replace('Scansionato con CamScanner', '').strip()
        
        # Sistema per intuire il genere dal titolo
        genere = "Varia"
        t_lower = titolo.lower()
        if "storia" in t_lower or "guerra" in t_lower: genere = "Storia"
        elif "filosofia" in t_lower: genere = "Filosofia"
        elif "diritto" in t_lower or "giustizia" in t_lower: genere = "Diritto"
        elif "romanzo" in t_lower or "poesia" in t_lower: genere = "Letteratura"
        
        # 3. Creiamo la scheda del libro
        libro = {
            "id": index,
            "titolo": titolo,
            "autore": autore,
            "anno": "N/D",           
            "editore": "N/D",        
            "genere": genere,       
            "disponibile": True,     
            "colore": colori[index % len(colori)], 
            "desc": f"Pagine: {pagine} | Codice Collocazione: {codice}"
        }
        catalogo_json.append(libro)

    # 4. Salviamo il file JSON
    with open(file_json, 'w', encoding='utf-8') as f:
        json.dump(catalogo_json, f, ensure_ascii=False, indent=4)
        
    print(f"\nMAGIA FATTA! Creato il file '{file_json}' con {len(catalogo_json)} libri pronti per il sito!")

# --- AVVIO DELLO SCRIPT ---
# Qui passiamo il tuo file Excel
FILE_EXCEL = 'CatalogoGS.xlsx' 
FILE_JSON = 'catalogo.json'

converti_excel_in_json(FILE_EXCEL, FILE_JSON)
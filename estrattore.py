import re
import json
from pypdf import PdfReader

def genera_json_catalogo(file_input_pdf, file_output_json):
    print("Sto leggendo il PDF originale per il sito web...")
    
    try:
        reader = PdfReader(file_input_pdf)
        testo_completo = ""
        for page in reader.pages:
            testo_estratto = page.extract_text()
            if testo_estratto:
                testo_completo += testo_estratto + "\n"
    except Exception as e:
        print(f"Errore durante la lettura del PDF: {e}")
        return

    testo_completo = testo_completo.replace('Scansionato con CamScanner', '')
    blocchi = re.split(r'\[[a-zA-Z0-9]\]\s*-?', testo_completo)

    catalogo_json = []
    
    # Colori per dare un bell'effetto grafico alternato alle schede del tuo sito
    colori = ["#1B3A5C", "#2E6DA4", "#C4622D", "#E8A838", "#3A6B4A", "#6B4C3B"]

    for i, blocco in enumerate(blocchi):
        b = re.sub(r'\s+', ' ', blocco).strip()
        if not b: continue
            
        try:
            if '/' not in b: continue
            parti_slash = b.split('/', 1)
            titolo = parti_slash[0].strip()
            resto = parti_slash[1]
            
            match_autore = re.search(r'(.*?)\.\s*-', resto)
            if not match_autore: continue
            autore = match_autore.group(1).strip()
            resto = resto[match_autore.end():]
            
            match_pagine = re.search(r'(\d+)\s*p\.', resto)
            pagine = match_pagine.group(1) if match_pagine else "N/D"
            
            if 'cm.' in resto:
                codice = resto.split('cm.')[-1].strip()
            else:
                codice = "N/D"
            
            # Piccolo sistema per intuire il genere
            genere = "Varia"
            t_lower = titolo.lower()
            if "storia" in t_lower or "guerra" in t_lower: genere = "Storia"
            elif "filosofia" in t_lower: genere = "Filosofia"
            elif "diritto" in t_lower or "giuridica" in t_lower: genere = "Diritto"
            
            libro = {
                "id": i,
                "titolo": titolo,
                "autore": autore,
                "anno": "N/D",           
                "editore": "N/D",        
                "genere": genere,       
                "disponibile": True,     
                "colore": colori[i % len(colori)], 
                "desc": f"Pagine: {pagine} | Codice Collocazione: {codice}"
            }
            catalogo_json.append(libro)
            
        except Exception:
            continue

    # Salviamo il file JSON
    with open(file_output_json, 'w', encoding='utf-8') as f:
        json.dump(catalogo_json, f, ensure_ascii=False, indent=4)
        
    print(f"MAGIA FATTA! Creato il file '{file_output_json}' con {len(catalogo_json)} libri pronti per il sito!")

# --- AVVIO DELLO SCRIPT ---
FILE_INPUT = 'Prima-parte-catalogo-1.pdf'  
FILE_OUTPUT = 'catalogo.json'
genera_json_catalogo(FILE_INPUT, FILE_OUTPUT)
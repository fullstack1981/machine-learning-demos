import os
import re
import json

# Basispfad zu Ihren Java-Dateien
verzeichnis = "traindata"
# Zielverzeichnis für Token-Dateien
ziel_verzeichnis = "traindata_tokens"
os.makedirs(ziel_verzeichnis, exist_ok=True)

def einfache_tokenisierung(text):
    # Einfache Tokenisierung basierend auf Leerzeichen und Sonderzeichen
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

def verarbeite_dateien(verzeichnis, ziel_verzeichnis):
    for i in range(1, 5000):
        basisname = f"MyClass{i}"
        pfad_old = os.path.join(verzeichnis, f"{basisname}_OLD.java")
        pfad_new = os.path.join(verzeichnis, f"{basisname}_NEW.java")

        # Lese den Inhalt der Dateien
        with open(pfad_old, 'r', encoding='utf-8') as f:
            inhalt_old = f.read()
        with open(pfad_new, 'r', encoding='utf-8') as f:
            inhalt_new = f.read()

        # Tokenisierung
        tokens_old = einfache_tokenisierung(inhalt_old)
        tokens_new = einfache_tokenisierung(inhalt_new)

        # Speichere die Tokens in einer JSON-Datei
        daten = {
            'old': tokens_old,
            'new': tokens_new
        }
        ziel_pfad = os.path.join(ziel_verzeichnis, f"{basisname}_tokens.json")
        with open(ziel_pfad, 'w', encoding='utf-8') as f:
            json.dump(daten, f, ensure_ascii=False, indent=4)

        print(f"Tokens für {basisname} gespeichert in {ziel_pfad}.")

verarbeite_dateien(verzeichnis, ziel_verzeichnis)

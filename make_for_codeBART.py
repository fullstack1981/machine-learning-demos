import os
import re

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
    ziel_pfad = os.path.join(ziel_verzeichnis, "alle_tokens.txt")
    with open(ziel_pfad, 'w', encoding='utf-8') as ziel_datei:
        for i in range(1, 5000 + 1):  # Angenommen, es gibt 5000 Klassenpaare
            basisname = f"MyClass{i}"
            pfad_old = os.path.join(verzeichnis, f"{basisname}_OLD.java")
            pfad_new = os.path.join(verzeichnis, f"{basisname}_NEW.java")

            # Lese den Inhalt der Dateien
            inhalt_old, inhalt_new = '', ''
            with open(pfad_old, 'r', encoding='utf-8') as f:
                inhalt_old = f.read()
            with open(pfad_new, 'r', encoding='utf-8') as f:
                inhalt_new = f.read()

            # Tokenisierung
            tokens_old = einfache_tokenisierung(inhalt_old)
            tokens_new = einfache_tokenisierung(inhalt_new)

            # Speichere die Tokens in der Textdatei im angepassten Format
            # Verwenden von "<|endoftext|>" als Trennzeichen zwischen OLD und NEW
            daten = ' '.join(tokens_old) + " <|endoftext|> " + ' '.join(tokens_new)
            ziel_datei.write(daten + "\n\n")

    print(f"Alle Tokens gespeichert in {ziel_pfad}.")

verarbeite_dateien(verzeichnis, ziel_verzeichnis)

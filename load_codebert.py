import transformers
from transformers import AutoModel, AutoTokenizer
import json
import os

from train_codeBART import tokenizer, model

# Pfad zum Verzeichnis mit den Token-Dateien
tokens_verzeichnis = "traindata_tokens"

# # Laden des Tokenizers und des Modells
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")

def lade_tokens(dateipfad):
    with open(dateipfad, 'r', encoding='utf-8') as f:
        daten = json.load(f)
    return daten

# Beispiel für das Laden und Verarbeiten einer spezifischen Token-Datei
beispiel_datei = os.path.join(tokens_verzeichnis, "MyClass1_tokens.json")
tokens_daten = lade_tokens(beispiel_datei)

# Tokenisierung des Java-Codes aus den gespeicherten Tokens
# Für die "alte" Version des Codes
tokens_alt = tokenizer(' '.join(tokens_daten['old']), return_tensors="pt")

# Für die "neue" Version des Codes
tokens_neu = tokenizer(' '.join(tokens_daten['new']), return_tensors="pt")

# Ausgabe der tokenisierten Versionen
print("Tokenisierte Version des alten Java-Codes:", tokens_alt)
print("Tokenisierte Version des neuen Java-Codes:", tokens_neu)

# Beispiel, wie man die Token-IDs zurück in lesbaren Text umwandelt (für die "alte" Version)
tokens_readable_alt = tokenizer.convert_ids_to_tokens(tokens_alt['input_ids'][0])
print("Lesbare Tokens (alt):", tokens_readable_alt)

# Beispiel, wie man die Token-IDs zurück in lesbaren Text umwandelt (für die "neue" Version)
tokens_readable_neu = tokenizer.convert_ids_to_tokens(tokens_neu['input_ids'][0])
print("Lesbare Tokens (neu):", tokens_readable_neu)


print(transformers.__version__)

# Angenommen, Sie haben einen Eingabecode, den Sie transformieren möchten
eingabe_code = ""

# Verwenden Sie den Tokenizer, um den Code in Tokens zu zerlegen
eingabe_tokens = tokenizer.encode(eingabe_code, return_tensors='pt')

# Verwenden Sie das Modell, um eine Vorhersage zu machen
ausgabe_tokens = model.generate(eingabe_tokens)

# Dekodieren Sie die Ausgabetokens zurück in Code
ausgabe_code = tokenizer.decode(ausgabe_tokens[0])

print(ausgabe_code)


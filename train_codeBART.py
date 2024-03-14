from torch.utils.data import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments, AutoModel, BartTokenizer, BartForConditionalGeneration
import os

class CodeDataset(Dataset):
    def __init__(self, file_path, tokenizer):
        self.tokenizer = tokenizer
        self.pairs = []

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            blocks = content.split('\n\n')

            print(f"Gefundene Blöcke: {len(blocks)}")  # Debug-Ausgabe

            for block in blocks:
                # Angenommen, '<|endoftext|>' trennt die Paare
                parts = block.split('<|endoftext|>')
                if len(parts) == 2:
                    old, new = parts
                    self.pairs.append((old.strip(), new.strip()))
                else:
                    print("Unerwartetes Format gefunden:", block[:100])  # Debug-Ausgabe für fehlerhafte Blöcke

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        source, target = self.pairs[idx]  # Ändere self.data zu self.pairs
        source_tokens = self.tokenizer(source, truncation=True, padding='max_length', max_length=512, return_tensors="pt")
        target_tokens = self.tokenizer(target, truncation=True, padding='max_length', max_length=512, return_tensors="pt")

        return {
            'input_ids': source_tokens['input_ids'].squeeze(0),
            'attention_mask': source_tokens['attention_mask'].squeeze(0),
            'labels': target_tokens['input_ids'].squeeze(0)
        }


# Tokenizer und Modell für BART laden
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large")

# CodeDataset, Trainer und TrainingArguments bleiben wie vorher definiert

# Erstellen Sie den Datensatz
train_dataset = CodeDataset('D:\\chel\\demos\\codebert\\traindata_tokens\\alle_tokens.txt', tokenizer)

# Erstellen Sie einen Trainer mit den angepassten TrainingArguments
training_args = TrainingArguments(
    output_dir='./results',          # Ausgabeverzeichnis
    num_train_epochs=3,              # Gesamtzahl der Trainingsepochen
    per_device_train_batch_size=16,  # Batchgröße pro Gerät während des Trainings
    per_device_eval_batch_size=64,   # Batchgröße für die Bewertung
    warmup_steps=500,                # Anzahl der Warmup-Schritte für den Lernratenplaner
    weight_decay=0.01,               # Gewichtsabbau, wenn wir etwas anderes als Null übergeben
    logging_dir='./logs',            # Verzeichnis für das Speichern von Protokollen
    logging_steps=100,               # Logging-Informationen werden alle 100 Schritte ausgegeben
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

# Starten Sie das Training
trainer.train()

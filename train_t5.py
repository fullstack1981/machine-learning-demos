import torch
from torch.utils.data import Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments

# Überprüfe, ob CUDA verfügbar ist, und setze das Gerät entsprechend
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Initialisiere den Tokenizer und das Modell
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Verschiebe das Modell auf die GPU, wenn verfügbar
model.to(device)

class CodeDataset(Dataset):
    def __init__(self, file_path, tokenizer):
        self.tokenizer = tokenizer
        self.pairs = []

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            blocks = content.split('\n\n')

            print(f"Gefundene Blöcke: {len(blocks)}")

            for block in blocks:
                parts = block.split('')
                if len(parts) == 2:
                    old, new = parts
                    self.pairs.append((old.strip(), new.strip()))
                else:
                    print("Unerwartetes Format gefunden:", block[:100])

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        source, target = self.pairs[idx]
        source_tokens = tokenizer(source, return_tensors="pt", max_length=512, padding="max_length", truncation=True)
        target_tokens = tokenizer(target, return_tensors="pt", max_length=512, padding="max_length", truncation=True)

        # Stelle sicher, dass Tensoren auf das richtige Gerät verschoben werden
        source_tokens = {k: v.to(device) for k, v in source_tokens.items()}
        target_tokens = {k: v.to(device) for k, v in target_tokens.items()}

        return {
            'input_ids': source_tokens['input_ids'].squeeze(0),
            'attention_mask': source_tokens['attention_mask'].squeeze(0),
            'labels': target_tokens['input_ids'].squeeze(0)
        }

# Erstelle den Datensatz
train_dataset = CodeDataset('D:\\chel\\demos\\codebert\\traindata_tokens\\alle_tokens.txt', tokenizer)

# TrainingArguments und Trainer bleiben unverändert
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    save_steps=500,
    per_device_train_batch_size=16,  # Möglicherweise kannst du diese Zahl erhöhen, wenn du eine leistungsstarke GPU hast
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=100,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

trainer.train()

# Speichern des Modells und des Tokenizers
model.save_pretrained('./results/final_model')
tokenizer.save_pretrained('./results/final_model')

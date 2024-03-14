from transformers import T5Tokenizer, T5ForConditionalGeneration

# Laden des gespeicherten Modells und Tokenizers
model_path = './results/final_model'
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

def predict_new_code(model, tokenizer, old_code):
    # Tokenize den "OLD" Code für das Modell
    inputs = tokenizer(old_code, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Generiere die Vorhersage
    output_sequences = model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=512,  # Anpassen für längere Ausgaben
        max_new_tokens=50,  # Steuert, wie viele neue Tokens maximal generiert werden sollen
        num_beams=4,  # Beam-Suche kann die Qualität der Ausgabe verbessern
        early_stopping=True
    )

    # Konvertiere die generierten Token-IDs zurück in Text
    new_code = tokenizer.decode(output_sequences[0], skip_special_tokens=True)

    return new_code

# Beispiel für "OLD" Java-Code
old_code_example = "public final class MyClass3_OLD protected short field0 protected byte field1 public void method0 public void method1"


# Verwende die Funktion, um "NEW" Code zu generieren
new_code_generated = predict_new_code(model, tokenizer, old_code_example)

print("Generierter 'NEW' Code:", new_code_generated)

import os
import random

anzahl_klassen = 5000

# Basis-Konfiguration
primitive_datentypen = ['int', 'long', 'double', 'boolean', 'char', 'byte', 'short']
objekt_datentypen = {
    'int': 'Integer', 'long': 'Long', 'double': 'Double', 'boolean': 'Boolean',
    'char': 'Character', 'byte': 'Byte', 'short': 'Short'
}
modifikatoren = ['public', 'protected', 'private']
weitere_modifikatoren = ['static', 'final', 'abstract', 'transient', 'volatile']
interfaces = ['Serializable', 'Cloneable', 'AutoCloseable', 'Runnable', 'Comparable', 'Iterable', 'Closeable', 'Flushable', 'Appendable', 'Readable']

def zufaelliger_modifikator(auswahl):
    return random.choice(auswahl)

def generiere_interfaces():
    anzahl_interfaces = random.randint(1, min(10, len(interfaces)))
    gewaehlte_interfaces = random.sample(interfaces, anzahl_interfaces)
    return ", ".join(gewaehlte_interfaces)

def generiere_alte_klasse(klasse_nummer):
    modifikator = zufaelliger_modifikator(modifikatoren)
    weitere_modifikator = random.choice(weitere_modifikatoren)
    klasse_name = f"MyClass{klasse_nummer:03}_OLD"
    erbt_von = "extends MyBaseClass" if random.choice([True, False]) else ""
    implementiert = f"implements {generiere_interfaces()}" if random.choice([True, False]) else ""

    felder = "\n".join([f"    {random.choice(modifikatoren)} {random.choice(primitive_datentypen)} field{i};" for i in range(random.randint(1, 4))])
    methoden = "\n".join([f"    public void method{i}() {{}}" for i in range(random.randint(1, 4))])

    klasse_struktur = f"{modifikator} {weitere_modifikator} class {klasse_name} {erbt_von} {implementiert} {{\n{felder}\n\n{methoden}\n}}\n"
    return klasse_name, klasse_struktur

def konvertiere_zu_neuer_klasse(klasse_name, alte_klasse_struktur):
    neue_klasse_struktur = alte_klasse_struktur
    for primitiv, objekt in objekt_datentypen.items():
        neue_klasse_struktur = neue_klasse_struktur.replace(f" {primitiv} ", f" {objekt} ")
    neue_klasse_struktur = neue_klasse_struktur.replace("_OLD {", "_NEW {").replace(klasse_name, f"{klasse_name[:-4]}_NEW")
    return f"{klasse_name[:-4]}_NEW", neue_klasse_struktur

verzeichnis = "traindata"
os.makedirs(verzeichnis, exist_ok=True)

for i in range(1, anzahl_klassen + 1):
    klasse_name_old, alte_klasse_struktur = generiere_alte_klasse(i)
    klasse_name_new, neue_klasse_struktur = konvertiere_zu_neuer_klasse(klasse_name_old, alte_klasse_struktur)

    # Speichere die alte Klasse
    with open(os.path.join(verzeichnis, f"{klasse_name_old}.java"), 'w') as file:
        file.write(alte_klasse_struktur)

    # Speichere die neue Klasse
    with open(os.path.join(verzeichnis, f"{klasse_name_new}.java"), 'w') as file:
        file.write(neue_klasse_struktur)

    print(f"{klasse_name_old}.java und {klasse_name_new}.java wurden im Verzeichnis '{verzeichnis}' gespeichert.")

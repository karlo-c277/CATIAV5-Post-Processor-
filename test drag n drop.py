
import os
import sys

# check if file was dropped on the script
if len(sys.argv) < 2:
    print("Odaberi i povuci .txt datoteku APT koda na tekst.")
    input("Klikni Enter za dalje...")
    exit()

# this is the file you dropped
input_file = sys.argv[1]

# provjeriti da li postoji file
if not os.path.exists(input_file):
    print("Nepostojeća datoteka.")
    input("Klikni Enter za dalje...")
    exit()


# provjeriti da li je file tekstualni
if not os.path.isfile(input_file):
    print("Neispravna datoteka.")
    input("Klikni Enter za dalje...")
    exit()

print("Datoteka učitana:", input_file)
print("Pretraživanje linija\n")

# provjeriti da li je zaista tekstualna datoteka
try:
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            print(line)
            
            
except UnicodeDecodeError:
    print("Nevaljana vrsta datoteke. Molimo odaberite tekstualnu datoteku.")
    input("Klikni Enter za dalje...")
    exit()
except Exception as e:
    print(f"Greška prilikom čitanja datoteke: {e}")
    input("Klikni Enter za dalje...")
    exit()

input("\nGotovo. Klikni Enter za zatvaranje...")
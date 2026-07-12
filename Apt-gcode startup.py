import os
import sys
import io

from parseline import Myparseline
from jezici import HR, EN
from output import OutputFilter

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, data):
        for f in self.files:
            f.write(data)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()

while True:
    izbor = input("Choose language (HR/EN): ").strip().upper()

    opcije_hr = ("HR", "1", "HRV", "HRVATSKI", "CRO")
    opcije_en = ("EN", "2", "ENG", "ENGLISH")

    if izbor in opcije_hr:
        LANG = HR
        break
    elif izbor in opcije_en:
        LANG = EN
        break
    else:
        print("- Invalid choice. Please enter HR or EN.")

print(LANG["def programa"])

while True:
    catia_comments = input(LANG["catia komentari"]).strip().upper()
    
    opcije_da = ("DA", "YES", "1")
    opcije_ne = ("NE", "NO", "0")

    if catia_comments in opcije_da:
        ccmt = 1
        break
    elif catia_comments in opcije_ne:
        ccmt = 0
        break
    else:
        print(LANG["kriv odabir da/ne"])
        
while True:
    input_file = input(LANG["unesite datoteku"]).strip()

    if not input_file.endswith(".txt"):
        input_file += ".txt"

    if not os.path.exists(input_file):
        print(LANG["Nepostojeća datoteka."] + "\n")
        continue

    if not os.path.isfile(input_file) or not input_file.lower().endswith(".txt"):
        print(LANG["Neispravna vrsta"] + "\n")
        continue
    break

print(LANG["Datoteka učitana:"], input_file)
print(LANG["Učitavanje linija"])
print("G55\nDIAMOF\n#DEFINIRATI SIROVAC")

parse = Myparseline(LANG, ccmt)
terminal_output = io.StringIO()
original_stdout = sys.stdout
sys.stdout = Tee(sys.stdout, terminal_output)

try:
    encp = ["utf-8",    "utf-8-sig",    "cp1250",   "iso-8859-2",   "latin-1"]
    for enc in encp:
        try:
            with open(input_file, "r", encoding=enc) as f:
                myline = ""
                for line in f:
                    myline += line.strip()
                    if myline.endswith("$"):
                        myline = myline[:-1]
                        continue
                    else:
                        parse.parseline(myline)
                        myline = ""
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(LANG["error"] + str(e))
            break
    print("\n" + LANG["Gotovo."])
finally:
    sys.stdout = original_stdout

output_lines = terminal_output.getvalue().splitlines(True)
filter_output = OutputFilter(LANG)
filter_output.save_filtered_output(output_lines)
exit(0)
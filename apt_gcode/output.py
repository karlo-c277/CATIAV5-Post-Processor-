
class OutputFilter:
    def __init__(self, LANG, preset):
        self.LANG = LANG
        self.preset = preset
    def save_filtered_output(self, output_lines):

        save_file = ""

        while save_file not in ["DA", "NE", "YES", "NO", "1", "0"]:

            save_file = input(self.LANG["save file y/n"]).strip().upper()

            if save_file in ["DA", "YES", "1"]:
                if self.preset == "1":
                    filename = input(self.LANG["naziv output fl"]).strip().split(".")[0] + ".MPF"

                    with open(filename, "w", encoding="utf-8") as file:
                        file.write("%_N_" + filename + "_MPF\n")
                        for line in output_lines:
                            if not line.strip().startswith("- "):
                                line = " ".join(line.split())
                                file.write(line.strip() + "\n")
                    print(self.LANG["spremljeno u"] + filename)
                    break
                else:
                    while True:
                        filename = input(self.LANG["naziv output fl"]).strip()
                        if "." not in filename:
                            while True:
                                ekstenzija = input(self.LANG["ekstenzija output"].strip())
                    
                                if ekstenzija == "":
                                    filename += ".txt"
                                    break
                                elif "." not in ekstenzija:
                                    filename += "." + ekstenzija
                                    break
                                elif ekstenzija.startswith("."):
                                    filename += ekstenzija
                                    break
                                else:
                                    continue
                            break                        
                        else:
                            if len(filename.split(".")) > 2 or len(filename.split(".")) == 1:
                                print(self.LANG["neispravni naziv"])
                                continue
                            else:
                                break
                    zaglavlje = input(self.LANG["zaglavlje output"]).strip()
                    encry = ""
                    while encry not in ("utf-8", "utf-8-sig", "cp1250", "iso-8859-2", "latin-1"):
                        encry = input(self.LANG["enkripcija"]).strip()

                    with open(filename, "w", encoding=encry) as file:
                        zaglavlje = zaglavlje.strip()
                        for line in output_lines:
                            if not line.strip().startswith("- "):
                                line = " ".join(line.split())
                                file.write(line.strip() + "\n")
                    print(self.LANG["spremljeno u"] + filename)
                    break
            elif save_file in ["NE", "NO", "0"]:
                print(self.LANG["ne zeli spremiti"])
            
            else:
                print(self.LANG["kriv odabir da/ne"])
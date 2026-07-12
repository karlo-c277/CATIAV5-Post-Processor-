class OutputFilter:
    def __init__(self, LANG):
        self.LANG = LANG

    def save_filtered_output(self, output_lines):

        save_file = ""

        while save_file not in ["DA", "NE", "YES", "NO", "1", "0"]:

            save_file = input(self.LANG["save file y/n"]).strip().upper()

            if save_file in ["DA", "YES", "1"]:
                
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

                with open(filename, "w", encoding="utf-8") as file:

                    for line in output_lines:
                        if not line.strip().startswith("- "):
                            file.write(line.strip())

                print(self.LANG["kraj"] + filename)

            elif save_file in ["NE", "NO", "0"]:
                print(self.LANG["kraj"])
            
            else:
                print(self.LANG["kriv odabir da/ne"])
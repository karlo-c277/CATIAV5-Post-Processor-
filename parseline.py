import re                                       #Omugućuje re.split() funkciju za razdvajanje stringa po više znakova
import math
# Tapping obavezno preko Output "CYCLE"
# Naziv, parametri, kompenzacije i svi podaci alata u CATIA-i se MORAJU poklapati sa onima u WinNC-u
class Myparseline:

    def __init__(self, LANG, ccmt, preset):
        self.LANG = LANG                        #Poziv ispisa na odabranom jeziku

        self.ccmt = ccmt                        #Varijabla koja određuje hoće li se komentari iz APT datoteke ispisati u izlaznoj datoteci
        
        self.ss = 3                             #Varijabla koju određuje korisnik ovisno o tome treba li se prilikom pokretanja vretena M03/M04 ispisivati okretaji ili ne
        
        self.preset = preset                    #Varijabla koja određuje hoće li se izlazna datoteka spremiti u MPF formatu ili ne
        
        self.lsmovement=""                      #Način kretanja alata
        self.lsplane=""                         #Ravnina xy, xz ili yz
        self.lsrotation=""                      #Smjer vrtnje vretena 
        self.ls_tip_rev=""                      #Način definiranja brzine vrtnje
        self.ls_tip_posmak=""                   #Način posmaka
        self.lssklop=""                         #Zadnji pozvani alat
        self.ls_x = 0.0                         #Zadnja x koordinata alata
        self.ls_y = 0.0                         #Zadnja y koordinata alata
        self.ls_z = 0.0                         #Zadnja z koordinata alata
        self.ls_i = 0.0                         #Zadnja vrijednost i vektora
        self.ls_j = 0.0                         #Zadnja vrijednost j vektora
        self.ls_k = 0.0                         #Zadnja vrijednost k vektora
        self.ls_spindle_speed = 0.0             #Zadnja vrijednost okretaja vretena
        self.ls_on_rotation = ""                #Zadnja vrijednost smjera vrtnje vretena
        self.ls_dim_typ = ""                    #Način definiranja koordinata (apsolutno / inkrementno)
        self.ls_clnt_typ = ""                   #Način podmazivanja (FLOOD / MIST)
        self.ls_clnt = ""                       #Zadnja definirana vrijednost podmazivanja (FLOOD / MIST / OFF)
        self.ls_cycle = ""                      #Zadnji definirani ciklus
        self.lsunits = "G21"                    #Mjerne jedinice
        self.komentari = ("TPRINT", "PPRINT","LOADTL/", "TOOLNO/", "REWIND/", "SELECTL/", "CUTTER/", "INTOL/", "OUTOL/", "TOLER/", "FINI", "END", "PARTNO", "$$", "OPERATION NAME", "TLAXIS", "CUTCOM")      #skraćivanje koda, na ovaj način se ne treba zapisivati line.startswith("comand_name") za svaku komandu posebno
        self.non_def = ("SWITCH/", "PPFUN", "GO/", "AUTOPS/", "INDIRP/")
        self.lsautops = 0
        self.ls_feed_speed = 0.0
        
        
    def parseline(self, line):
            
            if not line.strip():
                pass
                #preskakivanje praznih linija
            
            elif line.startswith("UNITS"):
                # Ensure the line contains a known unit; prompt until valid
                while not any(opt in line for opt in ("MM", "INCH", "1", "0", "IN")):
                    line = input(self.LANG["units"]).strip().upper()

                # Set measurement system and emit G-code only when changing
                if "MM" in line or "1" in line:
                    if self.lsunits != "G21":
                        print("G21")
                    self.lsunits = "G21"
                else:
                    if self.lsunits != "G20":
                        print("G20")
                    self.lsunits = "G20"
   
            elif self.ccmt ==1 and line.startswith("$$"):
                line = re.sub(r"\$+", "", line)
                print(f";{line}")
                #omogućuje da se linije označene sa $$ ispišu u izlaznoj datoteci kao komentari
                
            elif line.startswith(self.non_def):
                print(f"(nije def);{line}")
                
            elif self.ccmt==1 and line.startswith(self.komentari):
                
                if line.startswith("LOADTL/") or line.startswith("SELCTL/"):
                    tooln = line.split("/")
                    tool_slot = tooln[1].strip()
                    print(self.LANG["magazine slot"] + tool_slot)
                    
                elif line.startswith("CUTTER/"):
                    if len(line.split(" ")) < 3:
                        cutter = line.split("/")
                        r_ostrice = cutter[1].strip()
                        print(self.LANG["insert r"] + r_ostrice + "mm")
                    elif len(line.split(" ")) >= 3:
                        cutter = line.split(" ")
                        r_ostrice = cutter[1].strip()
                    
                elif line.startswith("INTOL/"):
                    intol = line.split("/")[1].strip()
                    print(self.LANG["intol"]+ intol + "mm")
                    
                elif line.startswith("OUTTOL/"):
                    outtol = line.split("/")[1].strip()
                    print(self.LANG["outtol"]+ outtol + "mm")
                    
                elif line.startswith("TOLER/"):
                    toler = line.split("/")[1].strip()
                    print(self.LANG["toler"]+ toler + "mm")
                    
                elif line.startswith("FINI") or line.startswith("END"):
                    print(self.LANG["kraj"])
                    
                elif line.startswith("PARTNO"):
                    line = line.split("PARTNO")[0].strip()
                    print(self.LANG["partno"] + line)
                
                elif line. startswith("OPERATION NAME"):
                    opname = line.split(":")
                    opname2 = opname[1].strip()

                    print(";" + opname2)
                
                elif line.startswith("TLAXIS"):
                    elements = line.split(" ")
                    print(self.LANG["tlaxis"] + " I" + elements[1].strip() + " J" + elements[2].strip() + " K" + elements[3].strip())
                
                else:
                    print("; " + line)
                #omogućuje da se linije označene sa navedenim komandama ispišu u izlaznoj datoteci po izboru korisnika kao komentari
            
            elif line.startswith("AUTOPS"):
                self.lsautops=1
                                     
            elif "CIRCLE" in line and self.lsautops==1:
                #kretanje alata po krucnici
                elements = re.split(r'[ ,/()]+', line)                          #izvacenje potrebnih podataka iz linije
                centar_x = float(elements[3].strip())
                centar_y = float(elements[4].strip())
                centar_z = float(elements[5].strip())
                #radius = elements[6].strip()
                centar2_x = float(elements[9].strip())
                centar2_y = float(elements[10].strip())
                centar2_z = float(elements[11].strip())
                kraj_x = float(elements[12].strip())
                kraj_y = float(elements[13].strip())
                kraj_z = float(elements[14].strip())
                
                if self.lsplane == "0":                                         
                    while True:                                                 #U INDIRV ako je jedinični vektor definiran preko 2 vektora onda se odmah dobiva podatak o ravnini, a ako je definiran preko jednog vektora onda se ovdje provjerava koji su centri luka isti i na temelju toga se određuje ravnina
                        if centar_x==kraj_x==self.ls_x:
                            self.lsplane="G19"
                            break
                        elif centar_y==kraj_y==self.ls_y:
                            self.lsplane="G18"
                            break
                        elif centar_z==kraj_z==self.ls_z:
                            self.lsplane="G17"
                            break
                        else:
                            print(self.LANG["promjena 3x koord"] + line)
                            continue
                    
                    print(self.lsplane)
                    
                kraj_x = round(float(kraj_x), 3)
                kraj_y = round(float(kraj_y), 3)
                kraj_z = round(float(kraj_z), 3)

                if centar_x!=centar2_x or centar_y!=centar2_y or centar_z!=centar2_z:
                    print(self.LANG["cta crc cent nije isti"], line)
                    #provjera ispravnosti podataka u apt file-u
                    
                if self.lsplane == "G18":
                    #odabir koordinata za kružnicu u xz ravini
                    vektor2_x=float(self.ls_x)-float(centar_x)
                    vektor2_z=float(self.ls_z)-float(centar_z)
                    D=float(self.ls_i)*vektor2_z-vektor2_x*float(self.ls_k)     #definiranje smjera kružnice (2D unakrsni produkt)
                    
                    vektor2_x=round(-(vektor2_x), 3)
                    vektor2_z=round(-(vektor2_z), 3)
                
                    if D<0:                                                     #definiranje smjera kružnog luka ovisno o smjeru unakrsnog produkta
                        movement="G2"
                    elif D>0:
                        movement="G3"
                    else:
                        print(self.LANG["sredina na tang"] + line)
                        
                    koord=f"X{kraj_x} Z{kraj_z} I{vektor2_x} K{vektor2_z}"
                    
                elif self.lsplane == "G17":
                    vektor2_y=float(self.ls_y)-float(centar_y)
                    vektor2_x=float(self.ls_x)-float(centar_x)
                    D=float(self.ls_i)*vektor2_y-vektor2_x*float(self.ls_j)

                    vektor2_y=round(-(vektor2_y), 3)
                    vektor2_x=round(-(vektor2_x), 3)
                    
                    if D<0:
                        movement="G2"
                    elif D>0:
                        movement="G3"
                    else:
                        print(self.LANG["sredina na tang"] + line)
                         
                    koord=f"X{kraj_x} Y{kraj_y} I{vektor2_x} J{vektor2_y}"
                    
                elif self.lsplane == "G19":
                    vektor2_y=float(self.ls_y)-float(centar_y)
                    vektor2_z=float(self.ls_z)-float(centar_z)
                    D=float(self.ls_j)*vektor2_z-vektor2_y*float(self.ls_k)

                    vektor2_y=round(-(vektor2_y), 3)
                    vektor2_z=round(-(vektor2_z), 3)  
                    
                    if D<0:
                        movement="G2"
                    elif D>0:
                        movement="G3"
                    else:
                        print(self.LANG["sredina na tang"] + line)
                    koord=f"Y{kraj_y} Z{kraj_z} J{vektor2_y} K{vektor2_z}"
                    
                else:
                    print(self.LANG["nepoznata ravnina"] + line)
            
                print(movement, koord, self.ls_feed_speed, self.ls_tip_posmak)
            
                self.ls_x=kraj_x
                self.ls_y=kraj_y
                self.ls_z=kraj_z
                self.lsmovement=movement
                self.lsautops=0
            
            elif line.startswith("GODLTA"):
                koord_x=""
                koord_y=""
                koord_z=""
                
                #definiranje incrementnog pomaka
                if self.ls_dim_typ != "G91":
                    print("G91", end=" ")
                    self.ls_dim_typ="G91"
                    
                coords = re.split(r'[,/]+', line)
                
                if len(coords)==4:
                    x = float(coords[1].strip())
                    y = float(coords[2].strip())
                    z = float(coords[3].strip())
                    
                elif len(coords)==2:
                    x = 0
                    y = 0
                    z = float(coords[1].strip())
                    
                else:
                    print(self.LANG["neispravan godlta"] + line)
                    return

                self.ls_x = round((self.ls_x + x), 3)   #definiranje novih koordinata alata u odnosu na prethodne koordinate obzirom da je inkrementni pomak, aidući pomak može biti apsolutni
                self.ls_y = round((self.ls_y + y), 3)
                self.ls_z = round((self.ls_z + z), 3)

                if x!=0:
                    koord_x="X"+str(x)
                if y!=0:
                    koord_y="Y"+str(y)
                if z!=0:
                    koord_z="Z"+str(z)
                
                print(koord_x, koord_y, koord_z)
        
            elif line.startswith("GOTO"):
                koord_x=""
                koord_y=""
                koord_z=""
                
                #definiranje apsolutnog pomaka
                if self.ls_dim_typ != "G90":
                    print("G90", end=" ")
                    self.ls_dim_typ="G90"
                
                coords = re.split(r'[,/]+', line)
                x = float(coords[1].strip())
                y = float(coords[2].strip())
                z = float(coords[3].strip())
                
                if x!=self.ls_x:
                    koord_x="X"+str(x)
                if y!=self.ls_y:
                    koord_y="Y"+str(y)
                if z!=self.ls_z:
                    koord_z="Z"+str(z)
                 
                print(koord_x, koord_y, koord_z)
                
                self.ls_x=x
                self.ls_y=y
                self.ls_z=z
                
            elif line.startswith("SPINDL"):
                if "OFF" in line:
                    rotation="OFF"
                    
                elif not ("ON" in line):
                    spindlDT = re.split(r'[,/]+', line)
                    if len(spindlDT)==4:
                        num = spindlDT[1].strip()
                        posmak_tip = spindlDT[2].strip()
                        rotation = spindlDT[3].strip()
                        
                        self.ls_spindle_speed = round(float(num), 3)

                        while posmak_tip not in ("SFM", "RPM"):
                            print(self.LANG["nepoznat posmak"] + line)
                            posmak_tip = input(self.LANG["posmak"]).strip().upper()
                        tipfedrejt = "G96 " if posmak_tip == "SFM" else "G97 "
                        self.ls_tip_rev = tipfedrejt.strip()

                        if self.ls_tip_rev != posmak_tip:
                            print(tipfedrejt, end=" ")
                            self.ls_tip_rev=tipfedrejt
                        print("S"+ str(round(float(num), 3)))
                           
                    else:
                        print(self.LANG["neispravni podaci"])
                    
                elif "ON" in line:
                    while True:
                        if self.preset == "0":
                            spindle_start = input(self.LANG["spindle start"]).strip().upper()
    
                            opcije_da = ("DA", "YES", "1")
                            opcije_ne = ("NE", "NO", "0")
                            if spindle_start in opcije_da:
                                self.ss = 1
                                break
                            elif spindle_start in opcije_ne:
                                self.ss = 0
                                break
                            else:
                                print(self.LANG["krivi spindle start"])
                        elif self.preset == "1":
                            self.ss = 0
                            break
                    
                    print(self.ls_on_rotation, end=" ")
                    if self.ss==1:
                        print("S"+ str(self.ls_spindle_speed)+ " " + self.ls_tip_rev)
                    
                while rotation not in ("CLW", "CCLW", "OFF"):
                    rotation = input(self.LANG["spindle m3/m4"] + f" ({line}) : ").strip().upper()

                smjer = {"CLW": "M3 ", "CCLW": "M4 ", "OFF": "M5 "}
                smjervrtnje = smjer[rotation]

                if rotation in ("CLW", "CCLW"):
                    self.ls_on_rotation = smjervrtnje
 
                if self.lsrotation != smjervrtnje:
                    print(smjervrtnje, end=" ")
                    
                    if smjervrtnje==("M5 "):
                        print(" ")
                        
                    self.lsrotation=smjervrtnje
                print("")    
                
            elif line.startswith("FEDRAT"):
                #if "RAPTO" in line:
                feed = re.split(r'[,/]+', line)
                numf = feed[1].strip()
                vrstaf = feed[2].strip()
            
                while vrstaf not in ("MMPR", "REV", "MMPM", "MIN"):
                    vrstaf = input(self.LANG["feedrat err"]).strip().upper()

                tip_posmak = "G95" if vrstaf in ("MMPR", "REV") else "G94"
    
                if self.ls_tip_posmak != tip_posmak:
                    print(tip_posmak, end=" ")
                    self.ls_tip_posmak = tip_posmak
                    
                movement="G1"
                
                if self.lsmovement != movement:
                        print(movement, end=" ")
                        self.lsmovement = movement
                
                print("F"+ str(round(float(numf), 3)))
                
            elif line.startswith("INDIRV"):
                vektor = re.split(r'[,/]+', line)
                self.ls_i=vektor[1].strip()
                self.ls_j=vektor[2].strip()
                self.ls_k=vektor[3].strip()
                
                if float(self.ls_i)!=0 and float(self.ls_j)!=0:
                    plane="G17"
                elif float(self.ls_i)!=0 and float(self.ls_k)!=0:
                    plane="G18"
                elif float(self.ls_j)!=0 and float(self.ls_k)!=0:
                    plane="G19"
                else:
                    plane="0"
                    
                if self.lsplane != plane:
                    print(plane, end=" ") if plane != "0" else None
                    self.lsplane=plane
                
            elif line.startswith("RAPID"):
                if self.lsmovement != "G0":
                    print("G0 ")
                    self.lsmovement="G0"
                
                #u starijim verzijama APT koda RAPUD se može spajati sa drugim komandama poput GOTO ili GODLTA    
                if "GOTO" in line:
                    if self.ls_dim_typ != "G90":
                        print("G90", end=" ")
                        self.ls_dim_typ="G90"
                    
                    elements = re.split(r'[ ,/]+', line)
                    x = float(elements[2].strip())
                    y = float(elements[3].strip())
                    z = float(elements[4].strip())                 
                
                    self.ls_x=x
                    self.ls_y=y
                    self.ls_z=z
                    
                elif "GODLTA" in line:
                    if self.ls_dim_typ != "G91":
                        print("G91", end=" ")
                        self.ls_dim_typ="G91"
                    
                    
                    elements = re.split(r'[,/]+', line)
                    
                    if len(elements)==4:
                        x = float(elements[2].strip())
                        y = float(elements[3].strip())
                        z = float(elements[4].strip())
                    elif len(elements)==2:
                        x = 0
                        y = 0
                        z = float(elements[2].strip())
                    else:
                        print(self.LANG["neispravan godlta"] + line)
                        
                    self.ls_x = round((self.ls_x + x), 3)
                    self.ls_y = round((self.ls_y + y), 3)
                    self.ls_z = round((self.ls_z + z), 3)
                    
                    print(koord_x, koord_y, koord_z)
                                                                                                
            elif line.startswith("COOLNT"):
                elements=line.split("/")
                clon=elements[1]
                
                while True:
                    if "OFF" in line or "FLOOD" in line or "MIST" in line or clon == "0" or clon == "1" or clon == "2" or clon == "3" or clon == "ON" or clon == "OFF" or clon == "FLOOD" or clon == "MIST":
                        clon=clon.strip().upper()
                        break
                    else:
                        clon = input(self.LANG["coolant on off"] + line + "--> : ").strip().upper()
                        continue
                    
                while True:
                    
                    if clon=="ON" or clon=="1":
                        while True:
                            if self.ls_clnt_typ=="":
                                print(self.LANG["coolant on off flood mist"] + line)
                                clon = input(self.LANG["ls-clnt"]).strip().upper()
                                break
                            elif self.ls_clnt_typ=="M8" or self.ls_clnt_typ=="M7" or self.ls_clnt_typ=="M9":
                                print(self.ls_clnt_typ)
                                continue
                        continue
                    elif clon=="OFF" or clon=="0":
                        print("M9")
                        self.ls_clnt="M9"
                        break
                    elif clon=="FLOOD" or clon=="2":
                        print("M8")
                        self.ls_clnt_typ="M8"
                        self.ls_clnt="M8"
                        break
                    elif clon=="MIST" or clon=="3":
                        print("M7")
                        self.ls_clnt_typ="M7"
                        self.ls_clnt="M7"
                        break
                    else:
                        print(self.LANG["coolant on off flood mist"] + line)
                        clon = input("").strip().upper()
                        continue
            
            elif line.startswith("DELAY") or line.startswith("DWELL"):
                delay=line.split("/")
                dwell=delay[1].strip()
                
                if "REV" in dwell:
                    dwell=dwell.split(",")
                    vrijeme=dwell[0].strip()
                    
                    print(f"G4 R{vrijeme}")
                else:
                    print(f"G4 S{round(float(dwell), 3)}")
            
            elif line.startswith("CYCLE/"):
                if "CYCLE/ON" in line:
                    if self.ls_cycle != "":
                        print(self.ls_cycle)
                    else:
                        print(self.LANG["Nema ciklusa"])
                     
                elif "TAP" in line:
                    tap = line.split(",")
                    dubina = tap[1].strip()
                    pitch = tap[2].strip()
               
                    while True:
                        if self.lsrotation == "M3 " or self.lsrotation == "CLW ":
                            returnsmj = "M4"
                            self.lsrotation = "M3 "
                            break
                        elif self.lsrotation == "M4 " or self.lsrotation == "CCLW ":
                            returnsmj = "M3"
                            self.lsrotation = "M4 "
                            break
                        else:
                            self.lsrotation = input(self.LANG["spindle m3/m4"]).strip().upper() + " "
                            continue
                 
                    povrsina = float(input(self.LANG["tap depth"] ).strip())
                       
                    depth = round((povrsina - float(dubina)), 3)
                 
                    while True:
                        holder = input(self.LANG["holder type"]).strip()
                        if holder == "0":
                            if self.ls_tip_rev == "SFM":
                                F = self.ls_spindle_speed * pitch
                            elif self.ls_tip_rev == "RPM":
                                F = pitch
                            else:
                                print(self.LANG["nepoznat posmak"] + line)
                            self.ls_cycle="G63 Z"+str(depth)+" F"+str(F)+" "+returnsmj
                            print(self.ls_cycle)
                            break
                        elif holder == "1":
                            self.ls_cycle="G331 Z"+str(depth)+" F"+str(pitch)+" \n G332 Z"+str(depth)+" "+returnsmj
                            print(self.ls_cycle)
                            break
                        else:
                            print(self.LANG[";Krivi broj"])
                            continue
                else:
                    print(self.LANG["neobradeni cycle"] + line)
                       
            else:
                print(self.LANG["Nepoznata naredba"], line)

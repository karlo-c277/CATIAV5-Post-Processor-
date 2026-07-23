import {write} from "./output.js";

console.log("parser")

export class MyParseline{
    constructor(settings){
            this.tolr_coord = 1e-3;
            this.lsmovement = "";
            this.lsplane = "";
            this.lsroation = "";
            this.ls_tip_rev = "";
            this.ls_tip_posmak = "";
            this.lssklop = "";
            this.ls_x = 0.0;
            this.ls_y = 0.0;
            this.ls_z = 0.0;
            this.ls_i = 0.0;
            this.ls_j = 0.0;
            this.ls_k = 0.0;
            this.ls_spindle_speed = 0.0;
            this.ls_on_rotation = "";
            this.ls_dim_typ = "";
            this.ls_clnt_typ = "";
            this.ls_cycle = "";
            this.lsunits = settings.output.default_units;
            this.comments = ["TPRINT", "PPRINT", "LOADTL/", "TOOLNO/", "REWIND/", "SELECTL/", "CUTTER/", "INTOL/", "OUTOL/", "TOLER/", "FINI", "END", "PARTNO", "OPERATION NAME", "TLAXIS", "CUTCOM"];
            this.non_def = ["SWITCH/", "PPFUN", "GO/", "INDIRP/"];
            this.lsautops = 0;
            this.ls_feed_speed = 0.0;
            this.ls_ls_x = 0.0;
            this.ls_ls_y = 0.0;
            this.ls_ls_z = 0.0;
            this.rapto=0;
            if (this.lsunits === "G21"){
                this.ls_units_word = "MM";
                this.rnd_num=3;
            }
            else if (this.lsunits === "G20"){
                this.ls_units_word = "INCH";
                this.rnd_num=4;
            }
            else {
                write("Unit value not determined")
            }
        }
    parseline(line){
            let elements;
            let centar_x;
            let centar_y;
            let centar_z;
            let centar2_x;
            let centar2_y;
            let centar2_z;
            let kraj_x;
            let kraj_y;
            let kraj_z;
            let vektor2_x;
            let vektor2_y;
            let vektor2_z;
            let D;
            let movement;
            let koord;
            let koord_x;
            let koord_y;
            let koord_z;
            let x;
            let y;
            let z;
            let dist;
            let ratio;
            let rdtx;
            let rdty;
            let rdtz;
            let koord__x;
            let koord__y;
            let koord__z;
            let dtx;
            let dty;
            let dtz;
            let spindlDT;
            let num;
            let rotation;
            let rotation_typ;
            let feednumf;
            let tool_slot;
            let cutter;
            let intol;
            let outol;
            let toler;
            let feed;
            let numf;
            let dwell;
            let revs;

        console.log(line);
        if (!line || !line.trim()) return;

        if (line.startsWith("UNITS")){
            if (line.includes("MM")){
                if (this.lsunits !== "G21"){
                    write("G21");
                    this.lsunits = "G21";
                }
            } else if (line.includes("INCH")){
                if (this.lsunits !== "G20"){
                    write("G20");
                    this.lsunits = "G20";
                }
            } else {
                write("Unknown unit type " + line);
            }
        }                          
        else if (this.non_def.some(word => line.startsWith(word))){
            write("not defined:" + line);
        }
        else if (this.comments.some(word => line.startsWith(word))){
            if (line.startsWith("LOADTL/") || line.startsWith("SELECTL/")){
                 tool_slot = line.split("/")[1].trim();
                write(";Magazine slot number: " + tool_slot);
            }
            else if (line.startsWith("CUTTER/")){
                let unit = (this.lsunits === "G21" || line.includes("MM")) ? "MM" : "INCH";
                if (line.split(/[,\/()]+/).length < 3){
                     cutter = line.split("/")[1].trim();
                    write(";Tool cutter radius: " + cutter + " " + unit);
                }
                else if (line.split(/[,\/()]+/).length >=3){
                     cutter = line.split("/")[1].trim();
                    write(";Tool cutter radius: " + cutter + " " + unit);
                }
            }
            else if (line.startsWith("INTOL/")){
                 intol = line.split("/")[1].trim();
                write(";Inside tolerance from the path: " + intol + this.ls_units_word);
            }
            else if (line.startsWith("OUTOL/")){
                 outtol = line.split("/")[1].trim();
                write(";Outside tolerance from the path: "+ outtol + this.ls_units_word);
            }
            else if (line.startsWith("TOLER/")){
                 toler = line.split("/")[1].trim();
                write(";Tolerance from the path: " + toler + this.ls_units_word);
            }
            else if (line.startsWith("FINI") || line.startsWith("END")){
                write(";End of program")
            }
            else if (line.startsWith("PARTNO")){
                 line = line.replace(/^PARTNO/, ";Part number: ");
                write(line);
            }
            else if (line.startsWith("OPERATION NAME")){
                 line = line.replace(/^OPERATION NAME/, ";").replace(/^:/, "");
                write(line);
            }
            else if (line.startsWith("TLAXIS")){
                 elements = line.split(" ");
                write(";Tool axies are I" + elements[1].trim() + " J" + elements[2].trim() + " K" + elements[3].trim());
            }
            else {
                write(";" + line);
            }
        }
        else if (line.startsWith("AUTOPS")){
            this.autops = 1;
        }
        else if (line.includes("CIRCLE") && this.lsautops === 1){
             elements = line.split(/[,\/()]+/).filter(Boolean);
             centar_x = +elements[3];
             centar_y = +elements[4];
             centar_z = +elements[5];
             centar2_x = +elements[9];
             centar2_y = +elements[10];
             centar2_z = +elements[11];
             kraj_x = +elements[12];
             kraj_y = +elements[13];
             kraj_z = +elements[14];

            if (this.lsplane === "0"){
                if (Math.abs(centar_x - kraj_x) <= this.tolr_coord && Math.abs(centar_x - this.ls_x) <= this.tolr_coord){
                    this.lsplane = "G19";
                }
                else if (Math.abs(centar_y - kraj_y) <= this.tolr_coord && Math.abs(centar_y - this.ls_y) <= this.tolr_coord){
                    this.lsplane = "G18";
                }
                else if (Math.abs(centar_z - kraj_z) <= this.tolr_coord && Math.abs(centar_z - this.ls_z) <= this.tolr_coord){
                    this.lsplane = "G17";
                }
                else {
                    write("ERROR CHANGE OF ALL 3 COORDINATES RE-DO THE APT OUTPUT " + line);
                }
                write(this.lsplane);
            }
            kraj_x = +kraj_x.toFixed(this.rnd_num);
            kraj_y = +kraj_y.toFixed(this.rnd_num);
            kraj_z = +kraj_z.toFixed(this.rnd_num);

            if (Math.abs(centar_x - centar2_x) <= this.tolr_coord || Math.abs(centar_y - centar2_y) <= this.tolr_coord || Math.abs(centar_z - centar2_z) <= this.tolr_coord){
                write("; ERROR Circle centers are not matching");
            }

            if (this.lsplane == "G18"){
                 vektor2_x = +this.ls_x - +centar_x;
                 vektor2_z = +this.ls_z - +centar_z;
                 D = +this.ls_i * vektor2_z - vektor2_x * +this.ls_k;
                
                vektor2_x = +vektor2_x.toFixed(this.rnd_num)
                vektor2_z = +vektor2_z.toFixed(this.rnd_num)


                if (D<0){
                     movement = "G2";
                }
                else if (D>0){
                     movement = "G3"
                }
                else {
                    write("ERROR CIRCLE CENTER IS ON THE CIRCLE TANGENT " + line)
                }

                 koord=(" X" + kraj_x + " Z" + kraj_z + " I" + vektor2_x + " K" + vektor2_z);
            }
            else if (this.lsplane == "G17"){
                 vektor2_x = +this.ls_x - +centar_x;
                 vektor2_y = +this.ls_y - +centar_y;
                 D = +this.ls_i * vektor2_y - vektor2_x * +this.ls_j;
                
                vektor2_x = +vektor2_x.toFixed(this.rnd_num)
                vektor2_y = +vektor2_y.toFixed(this.rnd_num)


                if (D<0){
                     movement = "G2";
                }
                else if (D>0){
                     movement = "G3"
                }
                else {
                    write("ERROR CIRCLE CENTER IS ON THE CIRCLE TANGENT " + line)
                }

                 koord=(" X" + kraj_x + " Y" + kraj_y + " I" + vektor2_x + " J" + vektor2_y);
            }
            else if (this.lsplane == "G19"){
                 vektor2_y = +this.ls_y - +centar_y;
                 vektor2_z = +this.ls_z - +centar_z;
                 D = +this.ls_j * vektor2_z - vektor2_y * +this.ls_k;
                
                vektor2_y = +vektor2_y.toFixed(this.rnd_num)
                vektor2_z = +vektor2_z.toFixed(this.rnd_num)


                if (D<0){
                     movement = "G2";
                }
                else if (D>0){
                     movement = "G3"
                }
                else {
                    write("ERROR CIRCLE CENTER IS ON THE CIRCLE TANGENT " + line)
                }

                 koord=(" Y" + kraj_Y + " Z" + kraj_z + " J" + vektor2_Y + " K" + vektor2_z);
            }
            write(movement, koord, this.ls_feed_speed, this.ls_tip_posmak);

            this.ls_x = kraj_x;
            this.ls_y = kraj_y;
            this.ls_z = kraj_z;
            this.lsmovement = movement;
            this.lsautops = 0;
        }
        else if (line.startsWith("GODLTA")){
             koord_x="";
             koord_y="";
             koord_z="";

            if (this.ls_dim_typ !== "G91"){
                write("G91");
                this.ls_dim_typ = "G91";
            }
             koord = line.split(/[,/]+/)
            if (koord.length === 4){
                 x = +koord[1];
                 y = +koord[2];
                 z = +koord[3];
            }
            else if (koord.length === 2){
                 x = 0;
                 y = 0;
                 z = +koord[1];
            }
            else {
                write("ERROR GODLTA ");
            }
            this.ls_x = (this.ls_x + x).toFixed(this.rnd_num);
            this.ls_y = (this.ls_y + y).toFixed(this.rnd_num);
            this.ls_z = (this.ls_z + z).toFixed(this.rnd_num);
            
            if (x !== 0){
                koord_x = " X" + x;
            }
            if (y !== 0){
                koord_y = " Y" + y;
            }
            if (z !== 0){
                koord_z = " Z" + z;
            }

            if (this.rapto === 1) {
                 dist = Math.hypot(x, y, z);
                 ratio = dist !== 0 ? this.rapto_num / dist : 0;
                 rdtx = ratio*x;
                 rdty = ratio*y;
                 rdtz = ratio*z;
                 koord__x = koord_x-rdtx;
                 koord__y = koord_y-rdty;
                 koord__z = koord_z-rdtz;

                write("G0 X" + koord__x + " Y" + koord__y + " Z" + koord__z + "\nG1");

                this.rapto = 0;
            }

            write(koord_x, koord_y, koord_z);

        }
        else if (line.startsWith("GOTO")){
             koord_x="";
             koord_y="";
             koord_z="";

            if (this.ls_dim_typ !== "G90"){
                write("G90");
                this.ls_dim_typ = "G90";
            }
             koord = line.split(/[,/]+/);
             x = +koord[1];
             y = +koord[2];
             z = +koord[3];

            if (x !== this.ls_x){
                 koord_x = " X" + x;
            }
            if (y !== this.ls_y){
                 koord_y = " Y" + y;
            }
            if (z !== this.ls_z){
                 koord_z = " Z" + z;
            }

            if (this.rapto === 1){
                 dtx = this.ls_x - x;
                 dty = this.ls_y - y;
                 dtz = this.ls_z - z;
                 dist = Math.hypot(dtx, dty, dtz);
                 ratio = dist !== 0 ? this.rapto_num / dist : 0;
                 rdtx = ratio*dtx;
                 rdty = ratio*dty;
                 rdtz = ratio*dtz;
                 koord__x = koord_x-rdtx;
                 koord__y = koord_y-rdty;
                 koord__z = koord_z-rdtz;

                write("G0 X" + koord__x + " Y" + koord__y + " Z" + koord__z + "\nG1");

                this.rapto = 0;
            }
            write(koord_x + koord_y + koord_z);
            
            this.ls_x=x;
            this.ls_y=y;
            this.ls_z=z;
        }
        else if (line.startsWith("SPINDL")){
            if (line.includes("OFF")){
                this.lsroation = "M5";
                write("M5");
            }
            else if (!line.includes("ON")){
                 spindlDT = line.split(/[,/]+/)
                if (spindlDT.length === 4){
                     num = spindlDT[1].trim();
                     rotation = spindlDT[3].trim();
                     rotation_typ = ""

                    this.ls_spindle_speed = parseFloat(num).toFixed(this.rnd_num)

                    if (line.includes("SFM")||line.includes("SMM")) {
                        rotation_typ = "G96";
                    }
                    else if (line.includes("RPM")){
                        rotation_typ = "G97";
                    }
                    else {
                        write("ERROR SPINDLE SPEED IS NOT DEFINED CORECTLY (SFM OR RPM) "+line);
                    }
                    if (this.ls_tip_rev !== rotation_typ){
                        this.ls_tip_rev = rotation_typ;
                    }
                    if (line.includes("CLW")){
                        this.lsrotation = "M3";
                    }
                    else if (line.includes("CCLW")){
                        this.lsrotation = "M4";
                    }
                    else {
                        write("ERROR SPINDLE DIRECTION NOT DEFINED " +line);
                    }
                    this.ls_on_rotation = ("S" + this.ls_spindle_speed + " " + this.ls_tip_rev + " " + this.lsrotation);
                    write(this.ls_on_rotation);
                }
                else {
                    write("ERROR SPINDLE DATA NOT VALID REQUIRES NUM VALUE SFM/SMM/RPM AND DIRECTION "+ line);
                }
            }
            else {
                write(this.ls_on_rotation);
            }
        }
        else if (line.startsWith("FEDRAT")){
            feed = line.split(/[,/]+/);
            numf = feed[1].trim();

            if (line.includes("MMPR")||line.includes("IPR")||line.includes("REV")){
                this.ls_tip_posmak = "G95";
            }
            else if (line.includes("MMPM")||line.includes("IPM")||line.includes("MIN")){
                this.ls_tip_posmak = "G96";
            }
             movement = "G1";
            if (this.lsmovement!==movement){
                write(movement);
                this.lsmovement = movement;
            }
            if (line.includes("RAPTO")){
                this.rapto=1;
                this.rapto_num = +feed[4]
            }
            write(this.ls_tip_posmak + " F" + numf);
        }
        else if (line.startsWith("RAPID")){
            write("G0");
            this.lsmovement = "G0";
            if (line.includes("GOTO")){
                 koord_x="";
                 koord_y="";
                 koord_z="";

                if (this.ls_dim_typ !== "G90"){
                    write("G90");
                    this.ls_dim_typ = "G90";
                }
                 koord = line.split(/[,/]+/);
                 x = +koord[1];
                 y = +koord[2];
                 z = +koord[3];

                if (x !== this.ls_x){
                     koord_x = " X" + x;
                }
                if (y !== this.ls_y){
                     koord_y = " Y" + y;
                }
                if (z !== this.ls_z){
                     koord_z = " Z" + z;
                }

                if (this.rapto === 1){
                     dtx = this.ls_x - x;
                     dty = this.ls_y - y;
                     dtz = this.ls_z - z;
                     dist = Math.hypot(dtx, dty, dtz);
                     ratio = dist !== 0 ? this.rapto_num / dist : 0;
                     rdtx = ratio*dtx;
                     rdty = ratio*dty;
                     rdtz = ratio*dtz;
                     koord__x = koord_x-rdtx;
                     koord__y = koord_y-rdty;
                     koord__z = koord_z-rdtz;

                    write("G0 X" + koord__x + " Y" + koord__y + " Z" + koord__z + "\nG1");

                    this.rapto = 0;
                }
                write(koord_x, koord_y, koord_z);
            
                this.ls_x=x;
                this.ls_y=y;
                this.ls_z=z;

            }
            else if (line.includes("GODLTA")){
                 koord_x="";
                 koord_y="";
                 koord_z="";

                if (this.ls_dim_typ !== "G91"){
                    write("G91");
                    this.ls_dim_typ = "G91";
                }
                koord = line.split(/[,/]+/)
                if (koord.length === 4){
                     x = +koord[1];
                     y = +koord[2];
                     z = +koord[3];
                }
                else if (koord.length === 2){
                     x = 0;
                     y = 0;
                     z = +koord[1];
                }
                else {
                    write("ERROR GODLTA ");
                }
                this.ls_x = (this.ls_x + x).toFixed(this.rnd_num);
                this.ls_y = (this.ls_y + y).toFixed(this.rnd_num);
                this.ls_z = (this.ls_z + z).toFixed(this.rnd_num);
                
                if (x !== 0){
                    koord_x = " X" + x;
                }
                if (y !== 0){
                    koord_y = " Y" + y;
                }
                if (z !== 0){
                    koord_z = " Z" + z;
                }

                if (this.rapto === 1) {
                     dist = Math.hypot(x, y, z);
                    ratio = dist !== 0 ? this.rapto_num / dist : 0;
                     rdtx = ratio*x;
                     rdty = ratio*y;
                     rdtz = ratio*z;
                     koord__x = koord_x-rdtx;
                     koord__y = koord_y-rdty;
                     koord__z = koord_z-rdtz;

                    write("G0 X" + koord__x + " Y" + koord__y + " Z" + koord__z + "\nG1");

                    this.rapto = 0;
                }

                write(koord_x, koord_y, koord_z);

            }

        }
        else if (line.startsWith("COOLNT")){
            if (line.includes("FLOOD")){
                this.ls_clnt_typ = "M8";
                write("M8");
            }
            else if (line.includes("MIST")){
                this.ls_clnt_typ = "M7";
                write("M7");
            }
            else if (line.includes("OFF")){
                write("M9");
            }
            else if (line.includes("ON")){
                if (this.ls_clnt_typ !== ""){
                    write(this.ls_clnt_typ);
                }
                else {
                    write("ERROR THERE IS NO PREDEFINED COOLANT TYPE, FUNTION ON CANNOT WORK");
                }
            }
        }
        else if (line.startsWith("DELAY")||line.startsWith("DWELL")){
            dwell=line.split("/");
            if (line.includes("REV")){
                revs=dwell.split(",").trim();
                write("G4 R" + revs);
            }
            else{
                write("G4 S" + +dwell.toFixed(3));
            }
        }
        else if (line.startsWith("CYCLE")){
            write(line);
        }
        else if (line.startsWith("$$")){
            line = line.split("$$")[1];
            write(";" + line);
        }
    }
}
/*{}
||
[]
\
^*/
console.log("parser end")
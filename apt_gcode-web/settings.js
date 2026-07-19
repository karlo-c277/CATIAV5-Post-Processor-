console.log("settings");
export function generateHeader(settings){
    return settings.output.header.replace("{filename}", settings.output.filename);
}
export function getSettings(){
    const preset = document.getElementById("preset").value;

    let settings = {
        preset: preset,
        output: {}
    };
    if (preset === "costum"){
        settings.output.filename = document.getElementById("filename").value;
        settings.output.encoding = document.getElementById("enc_output").value;
        settings.output.extension = document.getElementById("extension").value;
        settings.output.header = document.getElementById("output_header").value;
        settings.output.isoCommand = document.getElementById("command-to-iso").value;

    }
    else if (preset === "WinNC Sinumerik") {
        settings.output.filename = document.getElementById("filename").value;
        settings.output.encoding = "utf-8";
        settings.output.extension = ".mpf";
        settings.output.header = "%_N_{filename}_MPF";
        settings.output.isoCommand = "G291";
    }
    return settings;
}
export function validateSettings(){}

console.log("settings end")
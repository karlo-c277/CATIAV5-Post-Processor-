import { generateHeader } from "./apt_gcode-web/settings";

let output = [];
export function clearOutput(){
    output = [];
}
export function write(line){
    output.push(line);
}
export function getOutput(){
    return output.join("\n");
}
export function buildOutput(settings){
    let finalOutput = [];
    if (settings.output.header && settings.output.header.trim() !==""){
        finalOutput.push(generateHeader(settings));
    }
    if (settings.output.isoCommand && settings.output.isoCommand.trim() !==""){
        finalOutput.push(settings.output.isoCommand);
    }
    if (finalOutput.lengt > 0){
        finalOutput.push("");
    }
    finalOutput.push(...output);
    return finalOutput.join("\n");
}
function generateHeader(settings){
    return settings.output.header.replace("{filename}",settings.output.filename);
}
export function downloadOutput(text,settings){
    const blob = new Blob([text],{
        type:
        "text/plain;charset=" + settings.output.encoding
    });
    const link = document.createElement("a");
    link.herf=URL.createObjectURL(blob);
    link.download =
        settings.output.flename + settings.output.extension;
    link.click();
    URL.revokeObjectURL(link.herf);
}


console.log("output")
import { generateHeader } from "./settings.js";

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
    if (finalOutput.lenght > 0){
        finalOutput.push("");
    }
    finalOutput.push(...output);
    return finalOutput.join("\n");
}
export function downloadOutput(text,settings){
    const blob = new Blob([text],{
        type:
        "text/plain;charset=" + settings.output.encoding
    });
    const link = document.createElement("a");
    link.href=URL.createObjectURL(blob);
    link.download =
        settings.output.filename + settings.output.extension;
    link.click();
    URL.revokeObjectURL(link.href);
}
console.log("output end")

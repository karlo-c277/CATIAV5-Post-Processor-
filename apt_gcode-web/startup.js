console.log("startup")
import {getSettings, validateSettings} from "./settings.js";
console.log("1");
//import {MyParseline} from "./parseline.js";
console.log("2");
import {clearOutput, buildOutput, downloadOutput} from "./output.js";

document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("translateButton");
    button.addEventListener("click", translateAPT);});



async function translateAPT(){
    clearOutput();
    try {
        const settings = getSettings();
        validateSettings(settings);
        const aptText = await loadAPT(settings);
        const commands =splitAPT(aptText);
        const parser = new MyParseline(settings);
        for (const command of commands) {
            parser.parseLine(command);
        }
        const result = buildOutput(settings);
        document.getElementById("terminalOutput").textContent = result;
        if (settings.downloadOutput) {
            downloadOutput(result, settings);
        }
    }
    catch (error) {
        document.getElementById("terminalOutput").textContent=
            error.message;
        console.error(error);
    }
}
async function loadAPT(settings) {
    if (settings.file) {
        const buffer = await settings.file.arrayBuffer();
        const decoder = new TextDecoder(settings.inputEncoding);
        return decoder.decode(buffer);
    }
    if (settings.demo) {
        const response = await fetch("demo/"+settings.demo);
        if (!response.ok) {
            throw new Error("Demo file not found.");}
        return await response.text();
        const buffer = await response.arrayBuffer();
        const decoder = new TextDecoder(settings.inputEncoding);
        return decoder.decode(buffer);
    }
    throw new Error("No input file selected.");
}
function splitAPT(text) {
    const commands = [];
    const lines = text.split(/\r?\n/);
    let current = "";
    for (const line of lines) {
        current += line.trim();
        if (current.endsWith("$")){
            current = current.slice(0, -1);
            continue;
        }
        if (current !==""){
            commands.push(current);
        }
        current = "";
    }
    return commands;
}
console.log("startup end")
{}
[]
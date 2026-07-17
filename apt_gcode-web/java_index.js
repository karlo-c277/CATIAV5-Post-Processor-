export function getSettings(){
    const fileInput= document.getElementById("costumFilename");
    const demoSelect = document.getElementById("demoSelect");
    const settings = {
        file: fileInput.files[0] ?? null,
        demo: demoSelect.value,
        language: document.getElementById("language").value,
        aptVersion: document.getElementById("apt-code-version").value,
        preset: document.getElementById("preset").value,
        isoCommand: getElementById("command-to-iso").value.trim()
    };
    return settings;
}
export function validateSettings(settings) {
    if (!settings.file && !settings.demo){
        throw new Error ("Please select an APT file or a demo.");
    }
    if (settings.language === ""){
        throw new Error ("Please choose a language.");
    }
    if (settings.aptVersion === ""){
        throw new Error ("Please choose an APT code version.");
    }
    if (settings.preset === "") {
        throw new Error ("Please shoose an output preset.");
    }
    if (settings.preset === "costum" && settings.isoCommand ===""){
        throw new Error ("Enter the command to switch into ISO 6983.")
    }
    return true;
}

{}[0]
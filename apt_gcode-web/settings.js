document.addEventListener("DOMContentLoaded", ()=>{
    const presetSelect = document.getElementById("preset");
    const costumOptions = document.getElementById("costumOptions");
    presetSelect.addEventListener("change", () => {
        if (presetSelect.value === "costum") {
            costumOptions.style.display = "block";}
        else {
            costumOptions.style.display="none";
        }
    });
});

async function sendToPython(){
    const terminalOutput = document.getElementById("terminalOutput");
    const fileInput = document.getElementById("costumFilename");
    const demoSelect = document.getElementById("demoSelect").value;
    const language = document.getElementById("language").value;
    const aptVersion = document.getElementById("apt-code-version").value;
    const preset = document.getElementById("preset").value;
    const commandToIso = document.getElementById("command-to-iso").value;

    const formData = new FormData();
    formData.append("language", language);
    formData.append("aptVersion, aptVersion");
    formData.append("preset", preset);
    formData.append("commandToIso", commandToIso);

    if (fileInput.files[0]){
        formData.append("file", demoSelect);
        formData.append("isDemo", false)}
    else {
        formData.append("file", demoSelect);
        formData.append("isDemo", true);}

}


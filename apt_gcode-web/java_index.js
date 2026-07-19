console.log("index");
const presetSelect = document.getElementById("preset");
const costumOptions = document.getElementById("costumOptions");
const costumOutput = document.getElementById("costumOutput");
const downloadCheckbox = document.getElementById("downloadOutput");
const errorBox = document.getElementById("errorBox");

function updateCostumPanels() {
    const isCostum = presetSelect.value === "costum";
    const isDownload = downloadCheckbox.checked;

    costumOptions.style.display = "none";
    costumOutput.style.display= "none";

    if (isCostum) {
        costumOptions.style.display = "block";
        if (isDownload) {
            costumOutput.style.display = "block"
        }
    }
};
presetSelect.addEventListener(
    "change", updateCostumPanels
);
downloadCheckbox.addEventListener("change", updateCostumPanels);
updateCostumPanels();

console.log("index end")
async function predictDiabetes() {

    const data = {

        pregnancies: document.getElementById("pregnancies").value,

        glucose: document.getElementById("glucose").value,

        blood_pressure: document.getElementById("blood_pressure").value,

        skin_thickness: document.getElementById("skin_thickness").value,

        insulin: document.getElementById("insulin").value,

        bmi: document.getElementById("bmi").value,

        pedigree: document.getElementById("pedigree").value,

        age: document.getElementById("age").value
    };

    const resultBox = document.getElementById("resultBox");

    resultBox.innerHTML = "Analyzing Patient Data...";

    const response = await fetch("/predict", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)
    });

    const result = await response.json();

    resultBox.innerHTML = `
        Prediction: ${result.prediction}
        <br>
        Confidence: ${result.confidence}
    `;
}
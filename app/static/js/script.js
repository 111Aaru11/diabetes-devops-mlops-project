async function predictDiabetes() {
    // 1. Gather Data
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

    // 2. UI Elements
    const resultBox = document.getElementById("resultBox");
    const btn = document.getElementById("actionBtn");

    // 3. Loading State
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i> Analyzing Data...';
    
    // Clear previous classes
    resultBox.classList.remove("result-success", "result-danger");
    resultBox.innerHTML = `
        <div class="spinner-border text-cyan mb-3" role="status"></div>
        <div class="text-white">Running models via MLOps pipeline...</div>
    `;

    try {
        // 4. API Request (Unchanged from your original code)
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        // 5. Determine UI color based on prediction
        const predictionText = String(result.prediction).toUpperCase();
        let colorClass = "";
        let icon = "";

        // If prediction includes 'NON', it's safe (Green). Otherwise, danger (Red).
        if (predictionText.includes("NON")) {
            colorClass = "result-success";
            icon = '<i class="fa-solid fa-circle-check fs-1 mb-2"></i>';
        } else {
            colorClass = "result-danger";
            icon = '<i class="fa-solid fa-triangle-exclamation fs-1 mb-2"></i>';
        }

        // Apply classes and inject result HTML
        resultBox.classList.add(colorClass);
        resultBox.innerHTML = `
            ${icon}
            <div class="result-title">${predictionText}</div>
            <div class="result-confidence">Confidence Score: <strong>${result.confidence}</strong></div>
        `;

    } catch (error) {
        // Error handling
        resultBox.classList.add("result-danger");
        resultBox.innerHTML = `
            <i class="fa-solid fa-circle-xmark fs-1 mb-2"></i>
            <div class="result-title">System Error</div>
            <div class="result-confidence">Failed to connect to the prediction API.</div>
        `;
        console.error("Error:", error);
    } finally {
        // Reset Button
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-microscope me-2"></i> Predict Now';
        
        // Smooth scroll to the result box so the user sees it immediately
        resultBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
}
// async function predictDiabetes() {

//     const data = {

//         pregnancies: document.getElementById("pregnancies").value,

//         glucose: document.getElementById("glucose").value,

//         blood_pressure: document.getElementById("blood_pressure").value,

//         skin_thickness: document.getElementById("skin_thickness").value,

//         insulin: document.getElementById("insulin").value,

//         bmi: document.getElementById("bmi").value,

//         pedigree: document.getElementById("pedigree").value,

//         age: document.getElementById("age").value
//     };

//     const resultBox = document.getElementById("resultBox");

//     resultBox.innerHTML = "Analyzing Patient Data...";

//     const response = await fetch("/predict", {

//         method: "POST",

//         headers: {

//             "Content-Type": "application/json"
//         },

//         body: JSON.stringify(data)
//     });

//     const result = await response.json();

//     resultBox.innerHTML = `
//         Prediction: ${result.prediction}
//         <br>
//         Confidence: ${result.confidence}
//     `;
// }
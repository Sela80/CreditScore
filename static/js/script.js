document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('credit-form');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('result-container');
    const errorContainer = document.getElementById('error-container');
    const submitBtn = document.getElementById('submit-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset UI
        resultContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        loader.classList.remove('hidden');
        submitBtn.disabled = true;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Conversion des nombres
        const payload = {
            person_age: parseInt(data.person_age),
            person_income: parseFloat(data.person_income),
            person_home_ownership: data.person_home_ownership,
            person_emp_length: parseInt(data.person_emp_length),
            loan_intent: data.loan_intent,
            loan_amnt: parseFloat(data.loan_amnt),
            cb_person_default_on_file: data.cb_person_default_on_file,
            cb_person_cred_hist_length: parseInt(data.cb_person_cred_hist_length)
        };

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Erreur serveur");
            }

            const result = await response.json();
            displayResult(result);
        } catch (error) {
            displayError(error.message);
        } finally {
            loader.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });

    function displayResult(data) {
        const probPercent = (data.default_probability * 100).toFixed(2);
        resultContainer.innerHTML = `
            <h2>Résultat de l'évaluation</h2>
            <div class="result-item"><span class="result-label">Probabilité de défaut :</span> ${probPercent} %</div>
            <div class="result-item"><span class="result-label">Seuil expérimental :</span> ${(data.threshold * 100).toFixed(0)} %</div>
            <div class="result-item"><span class="result-label">Classe prédite :</span> ${data.predicted_class}</div>
            <p><em>Note : La probabilité est une estimation continue. La classe est une catégorisation binaire basée sur un seuil arbitraire. Ce résultat ne vaut pas décision d'octroi.</em></p>
            <p class="info-banner">${data.message}</p>
        `;
        resultContainer.classList.remove('hidden');
    }

    function displayError(message) {
        errorContainer.textContent = `Erreur : ${message}`;
        errorContainer.classList.remove('hidden');
    }
});
document.addEventListener('DOMContentLoaded', () => {
    // Accommodates Counter Logic
    const decBtn = document.getElementById('dec-accommodates');
    const incBtn = document.getElementById('inc-accommodates');
    const accInput = document.getElementById('accommodates');

    decBtn.addEventListener('click', () => {
        let val = parseInt(accInput.value);
        if (val > 1) {
            accInput.value = val - 1;
        }
    });

    incBtn.addEventListener('click', () => {
        let val = parseInt(accInput.value);
        if (val < 16) {
            accInput.value = val + 1;
        }
    });

    // Form Submission (Stabbing the ML connection)
    const form = document.getElementById('prediction-form');
    const priceDisplay = document.getElementById('predicted-price');
    const confidenceDisplay = document.getElementById('confidence-score');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // Visual feedback
        const btn = form.querySelector('.cta-button');
        const originalText = btn.innerText;
        btn.innerText = 'Calculating...';
        btn.disabled = true;

        // Real API Call
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(result => {
                if (result.error) {
                    alert('Error: ' + result.error);
                    return;
                }

                // Update UI
                animateValue(priceDisplay, 0, result.price, 1000);
                confidenceDisplay.innerText = result.confidence + '%';
            })
            .catch(error => {
                console.error('Error:', error);
                priceDisplay.innerText = 'Err';
            })
            .finally(() => {
                btn.innerText = originalText;
                btn.disabled = false;
            });
    });

    // Simple number animation function
    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
});

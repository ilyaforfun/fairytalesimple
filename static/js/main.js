document.addEventListener('DOMContentLoaded', function() {
    // Validate age input
    const ageInput = document.getElementById('child_age');
    if (ageInput) {
        ageInput.addEventListener('input', function() {
            const age = parseInt(this.value);
            if (age < 1) this.value = 1;
            if (age > 12) this.value = 12;
        });
    }

    // Validate name input
    const nameInput = document.getElementById('child_name');
    if (nameInput) {
        nameInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^a-zA-Z\s]/g, '');
        });
    }
});

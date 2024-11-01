document.addEventListener('DOMContentLoaded', function() {
    console.log('Story generator form initialized');
    
    const form = document.querySelector('form');
    const ageInput = document.getElementById('child_age');
    const nameInput = document.getElementById('child_name');
    const storyTypeSelect = document.getElementById('story_type');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const generateBtn = document.getElementById('generateBtn');
    
    // Validate age input
    if (ageInput) {
        console.log('Age input field found');
        ageInput.addEventListener('input', function() {
            const age = parseInt(this.value);
            if (age < 1) {
                console.log('Age below minimum, setting to 1');
                this.value = 1;
            }
            if (age > 12) {
                console.log('Age above maximum, setting to 12');
                this.value = 12;
            }
        });
    }

    // Validate name input
    if (nameInput) {
        console.log('Name input field found');
        nameInput.addEventListener('input', function() {
            const originalValue = this.value;
            const sanitizedValue = this.value.replace(/[^a-zA-Z\s]/g, '');
            if (originalValue !== sanitizedValue) {
                console.log('Removed invalid characters from name input');
            }
            this.value = sanitizedValue;
        });
    }

    // Form submission handling
    if (form) {
        console.log('Form element found');
        form.addEventListener('submit', function(e) {
            console.log('Form submission initiated');
            
            // Validate all fields
            const name = nameInput.value.trim();
            const age = parseInt(ageInput.value);
            const storyType = storyTypeSelect.value;
            
            let isValid = true;
            
            if (!name) {
                console.error('Name field is empty');
                isValid = false;
            }
            
            if (isNaN(age) || age < 1 || age > 12) {
                console.error('Invalid age value');
                isValid = false;
            }
            
            if (!storyType) {
                console.error('Story type not selected');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
                console.error('Form validation failed');
                return;
            }
            
            // Show loading indicator and disable submit button
            loadingIndicator.classList.remove('d-none');
            generateBtn.disabled = true;
            
            console.log('Form submission validated successfully', {
                name: name,
                age: age,
                storyType: storyType
            });
        });
    }
});

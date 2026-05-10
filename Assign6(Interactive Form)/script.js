document.getElementById('travelForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    // Clear previous messages
    clearErrors();
    clearMessage();

    // Get form values
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const destinations = Array.from(document.querySelectorAll('input[name="destinations"]:checked')).map(cb => cb.value);
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const travelers = document.getElementById('travelers').value;
    const budget = document.getElementById('budget').value;
    const interests = Array.from(document.querySelectorAll('input[name="interests"]:checked')).map(cb => cb.value);

    let isValid = true;

    // Validate name
    if (name === '') {
        showError('nameError', 'Full name is required.');
        isValid = false;
    }

    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email === '') {
        showError('emailError', 'Email is required.');
        isValid = false;
    } else if (!emailRegex.test(email)) {
        showError('emailError', 'Please enter a valid email address.');
        isValid = false;
    }

    // Validate phone
    const phoneRegex = /^\d{10}$/;
    if (phone === '') {
        showError('phoneError', 'Phone number is required.');
        isValid = false;
    } else if (!phoneRegex.test(phone)) {
        showError('phoneError', 'Please enter a valid 10-digit phone number.');
        isValid = false;
    }

    // Validate destinations
    if (destinations.length === 0) {
        showError('destinationsError', 'Please select at least one destination.');
        isValid = false;
    }

    // Validate dates
    if (startDate === '') {
        showError('startDateError', 'Start date is required.');
        isValid = false;
    }
    if (endDate === '') {
        showError('endDateError', 'End date is required.');
        isValid = false;
    } else if (startDate && endDate && new Date(startDate) >= new Date(endDate)) {
        showError('endDateError', 'End date must be after start date.');
        isValid = false;
    }

    // Validate travelers
    if (travelers === '' || travelers < 1) {
        showError('travelersError', 'Please enter a valid number of travelers.');
        isValid = false;
    }

    // Validate budget
    if (budget === '') {
        showError('budgetError', 'Please select a budget.');
        isValid = false;
    }

    // Validate interests
    if (interests.length === 0) {
        showError('interestsError', 'Please select at least one interest.');
        isValid = false;
    }

    // If valid, show success message with summary
    if (isValid) {
        const messageDiv = document.getElementById('message');
        messageDiv.innerHTML = `
            <h3>Trip Summary</h3>
            <p><strong>Name:</strong> ${name}</p>
            <p><strong>Email:</strong> ${email}</p>
            <p><strong>Phone:</strong> ${phone}</p>
            <p><strong>Destinations:</strong> ${destinations.join(', ')}</p>
            <p><strong>Dates:</strong> ${startDate} to ${endDate}</p>
            <p><strong>Travelers:</strong> ${travelers}</p>
            <p><strong>Budget:</strong> ${budget}</p>
            <p><strong>Interests:</strong> ${interests.join(', ')}</p>
            <p>Thank you for planning your Karnataka trip! We'll contact you soon.</p>
        `;
        messageDiv.style.color = 'green';
    }
});

function showError(elementId, message) {
    document.getElementById(elementId).textContent = message;
}

function clearErrors() {
    const errors = document.querySelectorAll('.error');
    errors.forEach(error => error.textContent = '');
}

function clearMessage() {
    document.getElementById('message').innerHTML = '';
}
document.getElementById('pepperForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get form values
    const formData = {
        robot_ip: document.getElementById('robot_ip').value.trim(),
        network_interface: document.getElementById('network_interface').value.trim(),
        language: document.querySelector('input[name="language"]:checked')?.value,
        priority_driver: document.querySelector('input[name="priority_driver"]:checked')?.value,
    };

    // Validate required fields
    if (!Object.values(formData).every(value => value)) {
        alert('Please fill all required fields');
        return;
    }

    // Send request
    fetch('/submit/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify(formData),
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Connection failed: ' + error.message);
    });
});
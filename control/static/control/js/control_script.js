 // Get the CSRF token from the hidden input field
 const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

 // Get language and rooms data from the hidden div
 const data = document.getElementById('data');
 const language = data.getAttribute("data-language");
 const rooms = JSON.parse(data.getAttribute("data-rooms"));
 console.log(rooms)
 
 // Get the driver select element
 const driverSelect = document.getElementById('driver-select');
 
 // Function to set the driver preference
 function setDriverPreference(priority_driver) {
     fetch('/set_driver/', {
         method: 'POST',
         headers: {
             'Content-Type': 'application/json',
             'X-CSRFToken': csrfToken,
         },
         body: JSON.stringify({
            priority_driver: priority_driver
         })
     })
     .then(response => response.json())
     .then(data => {
         console.log(data.message);
     })
     .catch(error => console.error('Error:', error));
 }

 driverSelect.addEventListener('change', function() {
    if (this.value) {
        console.log(this.value)
        setDriverPreference(this.value);
    } else {
        console.warn("No driver selected.");
    }
});

 
 
 // Toggle input zone visibility
 function toggleInputZone() {
     const inputZone = document.querySelector('.input-zone');
     inputZone.classList.toggle('hidden');
     inputZone.classList.toggle('show');
 }
 
 // Add event listeners for question and speech input
 const questionButton = document.querySelector('.send-question');
 questionButton.addEventListener('click', sendQuestion);
 
 document.getElementById('question-input').addEventListener('keypress', function(event) {
     if (event.key === 'Enter') {
         sendQuestion();
     }
 });
 
 const speechButton = document.querySelector('.send-speech');
 speechButton.addEventListener('click', sendSpeech);
 document.getElementById('speech-input').addEventListener('keypress', function(event) {
     if (event.key === 'Enter') {
         sendSpeech();
     }
 });
 
 // Add event listener for destination button
 document.querySelector('.destination-button').addEventListener('click', function() {
     const destination = document.getElementById('destination-input').value.trim();
     if (destination) {
         sendDestination(destination);
     } else {
         alert("Veuillez choisir une destination !");
     }
 });
document.getElementById('destination-input').addEventListener('keypress', function(event) {
    const destination = document.getElementById('destination-input').value.trim();
    if (destination) {
        if (event.key === 'Enter') {
            sendDestination(destination);
        }
    } else {
        alert("Veuillez choisir une destination !");
    }
});

 
 // Function to send move command
 function sendMove(move) {
     fetch('/move/', {
         method: 'POST',
         headers: {
             'Content-Type': 'application/json',
             'X-CSRFToken': csrfToken,  // Include the CSRF token
         },
         body: JSON.stringify({
             command_move: move,
         })
     })
     .then(response => response.json())
     .then(result => console.log(result.message))
     .catch(error => console.error('Error:', error));
 }
 
 // Function to switch tabs
 function switchTab(tabName) {
     document.querySelectorAll('.tab-button').forEach(button => {
         button.classList.remove('active');
     });
 
     document.querySelectorAll('.tab-content').forEach(content => {
         content.classList.add('hidden');
     });
 
     document.getElementById(`${tabName}-tab`).classList.remove('hidden');
     document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('active');
 }
 
 function sendQuestion() {
     const input = document.getElementById('question-input');
     const text = input.value.trim();
 
     if (text) {
         fetch('/question/', {
             method: 'POST',
             headers: {
                 'Content-Type': 'application/json',
                 'X-CSRFToken': csrfToken,  // Include the CSRF token
             },
             body: JSON.stringify({
                 question: text,
                 language: language,  // Ensure `language` is defined
             })
         })
         .then(response => {
             if (!response.ok) {
                 return response.text().then(text => {
                     throw new Error(`Network response was not ok. Status: ${response.status}, Body: ${text}`);
                 });
             }
             return response.json();
         })
         .then(data => {
             alert(data.message || "Commande envoyée !");
             input.value = '';
         })
         .catch(error => {
             console.error('Erreur:', error);
             alert('Une erreur s\'est produite. Veuillez réessayer.');
         });
     } else {
         alert("Veuillez écrire quelque chose pour que Pepper parle !");
     }
 }
 // Function to send speech
 function sendSpeech() {
     
     const input = document.getElementById('speech-input');
     const text = input.value.trim();
     if (text) {
         fetch('/speech/', {
             method: 'POST',
             headers: {
                 'Content-Type': 'application/json',
                 'X-CSRFToken': csrfToken,  // Include the CSRF token
             },
             body: JSON.stringify({
                 speech: text,
             })
         })
         .then(response => response.json())
         .then(data => {
             alert(data.message || "Commande envoyée !");
             input.value = '';
         })
         .catch(error => console.error('Erreur:', error));
     } else {
         alert("Veuillez écrire quelque chose pour que Pepper parle !");
     }
 }
 
 function sendSpeech() {
     const input = document.getElementById('speech-input');
     const text = input.value.trim();
 
     if (text) {
         fetch('/speech/', {
             method: 'POST',
             headers: {
                 'Content-Type': 'application/json',
                 'X-CSRFToken': csrfToken,  // Include the CSRF token
             },
             body: JSON.stringify({
                 speech: text,
             })
         })
         .then(response => {
             if (!response.ok) {
                 return response.text().then(text => {
                     throw new Error(`Network response was not ok. Status: ${response.status}, Body: ${text}`);
                 });
             }
             return response.json();
         })
         .then(data => {
             alert(data.message || "Commande envoyée !");
             input.value = '';
         })
         .catch(error => {
             console.error('Erreur:', error);
             alert('Une erreur s\'est produite. Veuillez réessayer.');
         });
     } else {
         alert("Veuillez écrire quelque chose pour que Pepper parle !");
     }
 }
 
 function sendDestination(destination) {
     fetch('/destination/', {
         method: 'POST',
         headers: {
             'Content-Type': 'application/json',
             'X-CSRFToken': csrfToken,  // Include the CSRF token
         },
         body: JSON.stringify({
             location: destination,
             rooms: rooms  // Ensure `rooms` is defined
         })
     })
     .then(response => {
         if (!response.ok) {
             return response.text().then(text => {
                 throw new Error(`Network response was not ok. Status: ${response.status}, Body: ${text}`);
             });
         }
         return response.json();
     })
     .then(result => {
         console.log(result.message);  // Log the message
     })
     .catch(error => {
         console.error('Erreur:', error);
         alert('Une erreur s\'est produite. Veuillez réessayer.');
     });
 }
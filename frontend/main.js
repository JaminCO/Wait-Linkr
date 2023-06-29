// Select the form element
const form = document.querySelector('form');
const url = 'https://wait-linkr-api.onrender.com/api/add';
// Add an event listener for form submission
form.addEventListener('submit', (e) => {
  // Prevent the form from submitting
  e.preventDefault();

  // Get the user's email address from the input element
  const email = document.querySelector('input[type="email"]').value;

  // Validate the email address
  if (!validateEmail(email)) {
    alert('Please enter a valid email address');
    return;
  }


const formData = new FormData();
formData.append('email', email);
formData.append('name', "Jamin");

fetch(url, {
  method : 'POST',
  body : formData,
  mode:"no-cors"
})
.then(response => {
  if (!response.ok) {
    // throw new Error('Network response was not ok');
  }
  // return response.json();
})
.then(data => {
  // console.log('API response:', data);
})
.catch(error => {
  // console.error('API error:', error);
});


alert('Form submitted successfully!');
form.reset();
});
// Email validation function
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
}

// Get the current year and update the footer text
const currentYear = new Date().getFullYear();
const footerText = document.querySelector('footer p');
footerText.innerHTML = `&copy; ${currentYear} WaitLinkr All rights reserved.`;

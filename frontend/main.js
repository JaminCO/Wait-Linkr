// Select the form element
const form = document.querySelector('form');
const url = 'http://127.0.0.1:5000/add';
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
console.log(email)


const formData = new FormData();
formData.append('email', email);

fetch(url, {
  method : 'POST',
  body : formData,
  mode:"no-cors"
})
.then(response => {
  console.log(response)
  if (response.ok) {
    console.log("Email added");
    alert("SUCCESS")
  } else {
    if (!response.ok) {
    console.log("Email not added");
    alert("testr")
    } 
   }
})
.catch(error=>{
  console.error(error)
  alert('Oops, something went wrong. Try again later.');
});
});
// Email validation function
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
}

// Get the current year and update the footer text
const currentYear = new Date().getFullYear();
const footerText = document.querySelector('footer p');
footerText.innerHTML = `&copy; ${currentYear} My Startup. All rights reserved.`;
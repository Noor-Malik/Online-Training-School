document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the form from refreshing the page

    // Show the loader
    document.getElementById('loader-wrapper').style.display = 'block';

    // Gather form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const userType = document.getElementById('userType').value;

    // Prepare the data for sending
    const data = {
        name: name,
        email: email,
        password: password,
        userType: userType
    };

    try {
        // Simulate an async call (e.g., to your backend API)
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json(); // Parse JSON response
        console.log(result); // You can handle the response here (e.g., display a success message)

        if (response.ok) {
            alert('Registration successful!');
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error('Error during registration:', error);
        alert('There was an issue with the registration.');
    } finally {
        // Hide the loader
        document.getElementById('loader-wrapper').style.display = 'none';
    }
});

// Function to open the form
function openForm() {
    document.getElementById("form-container").style.display = "block";
}

// Function to close the form
function closeForm() {
    document.getElementById("form-container").style.display = "none";
}

// Add event listener to form submission (optional)
document.getElementById("newForm").addEventListener("submit", function (e) {
    e.preventDefault();
    alert("Form submitted!");
    closeForm(); // Close the form after submission
});

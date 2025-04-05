document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");
    const loginForm = document.getElementById("loginForm");

    // Function to show messages
    function showMessage(message, type, container) {
        container.innerHTML = `<p class="${type}">${message}</p>`;
        setTimeout(() => { container.innerHTML = ""; }, 3000);
    }

    // Function to show/hide loading spinner
    function toggleLoading(isLoading, button) {
        if (isLoading) {
            button.innerHTML = "Processing...";
            button.disabled = true;
        } else {
            button.innerHTML = "Submit";
            button.disabled = false;
        }
    }

    // Handle Registration
    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const messageBox = document.getElementById("registerMessage");
            const submitBtn = registerForm.querySelector("button");

            toggleLoading(true, submitBtn);

            try {
                const response = await fetch("http://localhost:5000/api/auth/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password }),
                });

                const data = await response.json();
                toggleLoading(false, submitBtn);

                if (response.ok) {
                    showMessage("Registration Successful! Redirecting...", "success-message", messageBox);
                    setTimeout(() => { window.location.href = "login.html"; }, 2000);
                } else {
                    showMessage(data.message, "error-message", messageBox);
                }
            } catch (error) {
                toggleLoading(false, submitBtn);
                showMessage("Network Error! Try again.", "error-message", messageBox);
            }
        });
    }

    // Handle Login
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const messageBox = document.getElementById("loginMessage");
            const submitBtn = loginForm.querySelector("button");

            toggleLoading(true, submitBtn);

            try {
                const response = await fetch("http://localhost:5000/api/auth/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password }),
                });

                const data = await response.json();
                toggleLoading(false, submitBtn);

                if (response.ok) {
                    showMessage("Login Successful! Redirecting...", "success-message", messageBox);
                    setTimeout(() => { window.location.href = "dashboard.html"; }, 2000);
                } else {
                    showMessage(data.message, "error-message", messageBox);
                }
            } catch (error) {
                toggleLoading(false, submitBtn);
                showMessage("Network Error! Try again.", "error-message", messageBox);
            }
        });
    }
});

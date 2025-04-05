document.addEventListener("DOMContentLoaded", async () => {
    const listCropForm = document.getElementById("listCropForm");
    const cropList = document.getElementById("cropList");
    const messageBox = document.getElementById("messageBox"); // Element to show messages
    const loader = document.getElementById("cropLoader"); // Loader for crop list

    // Function to display messages
    function showMessage(text, isSuccess = true) {
        messageBox.textContent = text;
        messageBox.className = isSuccess ? "success-message" : "error-message";
        setTimeout(() => { messageBox.textContent = ""; }, 3000);
    }

    // Function to toggle the loader
    function toggleLoader(isLoading) {
        loader.style.display = isLoading ? "block" : "none";
    }

    // Function to fetch and display crops
    async function loadCrops() {
        toggleLoader(true); // Show loader
        try {
            const response = await fetch("http://localhost:5000/api/crop/list");
            if (!response.ok) throw new Error("Failed to load crops");

            const crops = await response.json();
            cropList.innerHTML = ""; // Clear previous crops

            crops.forEach(crop => {
                const cropCard = document.createElement("div");
                cropCard.className = "crop-card";

                cropCard.innerHTML = `
                    <h3>${crop.name}</h3>
                    <p>Type: <strong>${crop.type}</strong></p>
                    <p>Owner: ${crop.owner}</p>
                    ${crop.type === "resell" ? `<p>Price: ₹${crop.price}</p>` : ""}
                    ${crop.type === "barter" ? `<p>Exchange for: ${crop.exchange_for || "Any Crop"}</p>` : ""}
                    <button onclick="barterOrBuy('${crop.id}', '${crop.type}')">
                        ${crop.type === "barter" ? "Barter Now" : "Buy Now"}
                    </button>
                `;

                cropList.appendChild(cropCard);
            });

            showMessage("Crops loaded successfully!", true);
        } catch (error) {
            cropList.innerHTML = "<p class='error-message'>Error loading crops. Try again later.</p>";
            console.error("Error fetching crops:", error);
        } finally {
            toggleLoader(false); // Hide loader
        }
    }

    // Handle crop listing form submission
    listCropForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const owner = document.getElementById("owner").value;
        const name = document.getElementById("cropName").value;
        const type = document.getElementById("cropType").value;
        const price = document.getElementById("price").value || null;
        const exchangeFor = document.getElementById("exchangeFor").value || null;
        const submitBtn = listCropForm.querySelector("button");

        // Disable button & show loading
        submitBtn.innerHTML = "Listing...";
        submitBtn.disabled = true;

        try {
            const response = await fetch("http://localhost:5000/api/crop/add", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ owner, name, type, price, exchange_for: exchangeFor }),
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.message);

            showMessage("Crop listed successfully!", true);
            listCropForm.reset();
            loadCrops();
        } catch (error) {
            showMessage(error.message, false);
        } finally {
            submitBtn.innerHTML = "List Crop";
            submitBtn.disabled = false;
        }
    });

    // Handle barter or buy action
    window.barterOrBuy = async (id, type) => {
        const endpoint = type === "barter" ? `crop/barter/${id}` : `crop/buy/${id}`;
        try {
            const response = await fetch(`http://localhost:5000/api/${endpoint}`, { method: "POST" });
            const data = await response.json();
            if (!response.ok) throw new Error(data.message);

            showMessage(data.message, true);
            loadCrops();
        } catch (error) {
            showMessage(error.message, false);
        }
    };

    loadCrops();
});

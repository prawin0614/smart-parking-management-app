const API_URL = "http://127.0.0.1:8000";


// =========================================================
// Load Parking Slots
// =========================================================

async function loadSlots() {

    const container = document.getElementById("slotContainer");

    container.innerHTML = `
        <div class="loading">
            Loading parking slots...
        </div>
    `;

    try {

        const response = await fetch(`${API_URL}/slots`);

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || "Failed to load parking slots");
        }

        const slots = result;

        displaySlots(slots);
        updateStatistics(slots);

    } catch (error) {

        console.error(error);

        container.innerHTML = `
            <div class="error-message">
                Unable to load parking slots: ${error.message}
            </div>
        `;
    }
}


// =========================================================
// Display Slots
// =========================================================

function displaySlots(slots) {

    const container = document.getElementById("slotContainer");

    if (slots.length === 0) {

        container.innerHTML = `
            <div class="empty-state">
                <h3>No Parking Slots</h3>
                <p>Add your first parking slot to get started.</p>
            </div>
        `;

        return;
    }


    container.innerHTML = slots.map(slot => {

        const isOccupied = slot.status === "OCCUPIED";

        return `
            <div class="slot-card">

                <div class="slot-top">

                    <div class="slot-number">
                        ${slot.slot_number}
                    </div>

                    <div class="slot-status ${isOccupied ? "occupied" : "available"}">
                        ${slot.status}
                    </div>

                </div>


                <div class="slot-info">

                    <div class="slot-info-row">
                        <span>Vehicle Type</span>
                        <span>${slot.vehicle_type}</span>
                    </div>

                    <div class="slot-info-row">
                        <span>Slot ID</span>
                        <span>#${slot.id}</span>
                    </div>

                </div>


                <div class="slot-actions">

                    <button
                        class="toggle-btn"
                        onclick="toggleSlot(${slot.id}, '${slot.status}')"
                    >
                        ${isOccupied ? "Make Available" : "Occupy Slot"}
                    </button>

                    <button
                        class="delete-btn"
                        onclick="deleteSlot(${slot.id})"
                    >
                        Delete
                    </button>

                </div>

            </div>
        `;

    }).join("");
}


// =========================================================
// Update Dashboard Statistics
// =========================================================

function updateStatistics(slots) {

    const total = slots.length;

    const occupied = slots.filter(
        slot => slot.status === "OCCUPIED"
    ).length;

    const available = slots.filter(
        slot => slot.status === "AVAILABLE"
    ).length;


    document.getElementById("totalSlots").textContent = total;

    document.getElementById("availableSlots").textContent = available;

    document.getElementById("occupiedSlots").textContent = occupied;
}


// =========================================================
// Add Parking Slot
// =========================================================

document.getElementById("slotForm").addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        const slotNumber =
            document.getElementById("slotNumber").value.trim();

        const vehicleType =
            document.getElementById("vehicleType").value;


        if (!slotNumber || !vehicleType) {
            alert("Please fill all fields.");
            return;
        }


        try {

            const response = await fetch(`${API_URL}/slots`, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    slot_number: slotNumber,
                    vehicle_type: vehicleType
                })

            });


            const result = await response.json();


            if (!response.ok) {
                throw new Error(result.message || "Failed to add slot");
            }


            alert("Parking slot added successfully.");

            document.getElementById("slotForm").reset();

            closeModal();

            loadSlots();


        } catch (error) {

            console.error(error);

            alert(error.message);
        }

    }
);


// =========================================================
// Occupy / Make Available
// =========================================================

async function toggleSlot(slotId, currentStatus) {

    const newStatus =
        currentStatus === "AVAILABLE"
            ? "OCCUPIED"
            : "AVAILABLE";


    try {

        const response = await fetch(
            `${API_URL}/slots/${slotId}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    status: newStatus
                })
            }
        );


        const result = await response.json();


        if (!response.ok) {
            throw new Error(
                result.message || "Failed to update slot"
            );
        }


        loadSlots();


    } catch (error) {

        console.error(error);

        alert(error.message);
    }
}


// =========================================================
// Delete Parking Slot
// =========================================================

async function deleteSlot(slotId) {

    const confirmed = confirm(
        "Are you sure you want to delete this parking slot?"
    );


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/slots/${slotId}`,
            {
                method: "DELETE"
            }
        );


        const result = await response.json();


        if (!response.ok) {
            throw new Error(
                result.message || "Failed to delete slot"
            );
        }


        loadSlots();


    } catch (error) {

        console.error(error);

        alert(error.message);
    }
}


// =========================================================
// Modal
// =========================================================

function openModal() {

    const modal = document.getElementById("modal");

    modal.classList.add("show");

    document.getElementById("slotNumber").focus();
}


function closeModal() {

    const modal = document.getElementById("modal");

    modal.classList.remove("show");
}


// =========================================================
// Close Modal When Clicking Outside
// =========================================================

document.getElementById("modal").addEventListener(
    "click",
    function(event) {

        if (event.target === this) {
            closeModal();
        }

    }
);


// =========================================================
// Close Modal With Escape Key
// =========================================================

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Escape") {
            closeModal();
        }

    }
);


// =========================================================
// Start Application
// =========================================================

loadSlots();

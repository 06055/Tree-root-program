document.addEventListener("DOMContentLoaded", function () {

    const modalButtons = document.querySelectorAll("[data-modal]");



    const closeButtons = document.querySelectorAll(".close");


    const modals = document.querySelectorAll(".modal");


    modalButtons.forEach(button => {
        button.addEventListener("click", () => {
            const modalId = button.getAttribute("data-modal");
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = "block";
            }
        });
    });

    closeButtons.forEach(button => {
        button.addEventListener("click", () => {
            const modalId = button.getAttribute("data-close");
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = "none";
            }
        });
    });


    window.addEventListener("click", (event) => {
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    });


    const form = document.getElementById("coreForm");
    if (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            const formData = new FormData(form);

            const response = await fetch("/three_in_add", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();

            if (result.success) {
                alert("Core added successfully!");
                form.reset();
                document.getElementById("modalAddCore").style.display = "none";
                location.reload(); 
            } else {
                alert("Error: " + result.message);
            }
        });
    }
});

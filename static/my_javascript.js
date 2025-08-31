document.addEventListener("DOMContentLoaded", function () {

    const openModalButton = document.getElementById("openModal");
    const modal = document.getElementById("myModal");

    const closeButton = modal.querySelector(".close");

    openModalButton.addEventListener("click", () => {
        modal.style.display = "block";
    });

    closeButton.addEventListener("click", () => {
        modal.style.display = "none";
    });

    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    const form = document.getElementById("coreForm");
    if (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            const formData = new FormData(form);

            try {
                const response = await fetch("/three_in_add", {
                    method: "POST",
                    body: formData,
                });

                if (!response.ok) {
                    alert("Network error: " + response.status);
                    return;
                }

                const result = await response.json();

                if (result.success) {
                    alert("Core added successfully!");
                    form.reset();
                    modal.style.display = "none";
                    location.reload();
                } else {
                    alert("Error: " + result.message);
                }
            } catch (error) {
                alert("Fetch error: " + error);
            }
        });
    }
});

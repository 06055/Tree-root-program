document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-modal]").forEach(button => {
        button.addEventListener("click", () => {
            const id = button.getAttribute("data-modal");
            const modal = id ? document.getElementById(id) : null;
            if (modal) modal.style.display = "block";
        });
    });

    const legacyOpen = document.getElementById("openModal");
    const legacyModal = document.getElementById("myModal");
    if (legacyOpen && legacyModal) {
        legacyOpen.addEventListener("click", () => {
            legacyModal.style.display = "block";
        });
    }

    document.querySelectorAll(".close").forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-close");
            if (targetId) {
                const m = document.getElementById(targetId);
                if (m) m.style.display = "none";
            } else {
                const modal = btn.closest(".modal");
                if (modal) modal.style.display = "none";
            }
        });
    });

    window.addEventListener("click", event => {
        if (event.target && event.target.classList && event.target.classList.contains("modal")) {
            event.target.style.display = "none";
        }
    });

    document.addEventListener("keydown", event => {
        if (event.key === "Escape") {
            document.querySelectorAll(".modal").forEach(m => m.style.display = "none");
        }
    });

    const form = document.getElementById("coreForm");
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(form);

            try {
                const resp = await fetch(form.action || window.location.href, {
                    method: form.method || "POST",
                    body: formData,
                });

                if (!resp.ok) {
                    alert("Network error: " + resp.status);
                    return;
                }

                const result = await resp.json();
                if (result.success) {
                    alert("Успешно!");
                    form.reset();
                    const addModal = document.getElementById("modalAddCore");
                    if (addModal) addModal.style.display = "none";
                    else document.querySelectorAll(".modal").forEach(m => m.style.display = "none");
                    location.reload();
                } else {
                    alert("Ошибка: " + (result.message || "unknown"));
                }
            } catch (err) {
                alert("Fetch error: " + err);
            }
        });
    }

    window.showModalById = id => {
        const m = document.getElementById(id);
        if (m) m.style.display = "block";
    };
    window.hideModalById = id => {
        const m = document.getElementById(id);
        if (m) m.style.display = "none";
    };
});


document.querySelectorAll(".modal_window_for_cores").forEach(button => {
    button.addEventListener("click", () => {
        const coreName = button.getAttribute("data-core");
        const hiddenInput = document.querySelector("#modalCoreInfo input[name='thecores']");
        if (hiddenInput) hiddenInput.value = coreName; 
    });
});

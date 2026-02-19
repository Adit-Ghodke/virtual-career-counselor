/* ── Virtual Career Counselor v3.0 — Client-side JS ──────────────── */

document.addEventListener("DOMContentLoaded", () => {
    // Show loading state on form submit buttons
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
        form.addEventListener("submit", () => {
            const btn = form.querySelector("#searchBtn");
            if (btn) {
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Generating…';
                btn.classList.add("loading");
            }
        });
    });

    // Auto-dismiss flash alerts after 5 seconds
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach((alert) => {
        setTimeout(() => {
            const closeBtn = alert.querySelector(".btn-close");
            if (closeBtn) closeBtn.click();
        }, 5000);
    });

    // ── Dark Mode Toggle ─────────────────────────────────────────
    const toggle = document.getElementById("darkModeToggle");
    const icon = document.getElementById("darkModeIcon");
    const html = document.documentElement;

    // Load saved preference
    const savedTheme = localStorage.getItem("theme") || "light";
    html.setAttribute("data-bs-theme", savedTheme);
    updateDarkModeIcon(savedTheme);

    if (toggle) {
        toggle.addEventListener("click", (e) => {
            e.preventDefault();
            const current = html.getAttribute("data-bs-theme");
            const next = current === "dark" ? "light" : "dark";
            html.setAttribute("data-bs-theme", next);
            localStorage.setItem("theme", next);
            updateDarkModeIcon(next);
        });
    }

    function updateDarkModeIcon(theme) {
        if (icon) {
            icon.className = theme === "dark" ? "bi bi-sun-fill" : "bi bi-moon-fill";
        }
    }
});


// ── Voice Input (Web Speech API) ─────────────────────────────────

function startVoiceInput(inputId) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert("Voice input is not supported in this browser. Try Chrome or Edge.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    const inputEl = document.getElementById(inputId);
    const micBtn = inputEl ? inputEl.nextElementSibling : null;

    if (micBtn) {
        micBtn.classList.add("btn-danger", "voice-recording");
        micBtn.classList.remove("btn-outline-secondary");
    }

    recognition.start();

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (inputEl) {
            inputEl.value = inputEl.value ? inputEl.value + " " + transcript : transcript;
            inputEl.focus();
        }
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        if (event.error === "not-allowed") {
            alert("Microphone access denied. Please allow microphone permissions.");
        }
    };

    recognition.onend = () => {
        if (micBtn) {
            micBtn.classList.remove("btn-danger", "voice-recording");
            micBtn.classList.add("btn-outline-secondary");
        }
    };
}

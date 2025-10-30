// List of supported languages
const languages = [
  { code: "en", name: "English" },
  { code: "ta", name: "தமிழ்" }
  // Add other languages: "as", "bn", "gu", etc.
];

// Function to set language
function setLanguage(lang) {
  localStorage.setItem("language", lang);
  updateContent();
}

// Function to update page content
function updateContent() {
  const lang = localStorage.getItem("language") || "en";
  const elements = document.querySelectorAll("[data-i18n]");
  elements.forEach(element => {
    const key = element.getAttribute("data-i18n");
    element.textContent = translations[lang][key] || element.textContent;
  });
  // Update placeholder attributes
  const inputs = document.querySelectorAll("input[data-i18n-placeholder], select[data-i18n-placeholder]");
  inputs.forEach(input => {
    const key = input.getAttribute("data-i18n-placeholder");
    input.placeholder = translations[lang][key] || input.placeholder;
  });
  // Update button values
  const buttons = document.querySelectorAll("button[data-i18n-value]");
  buttons.forEach(button => {
    const key = button.getAttribute("data-i18n-value");
    button.textContent = translations[lang][key] || button.textContent;
  });
}

// Populate language dropdown
function populateLanguageDropdown() {
  const languageSelect = document.getElementById("language");
  if (languageSelect) {
    languages.forEach(lang => {
      const option = document.createElement("option");
      option.value = lang.code;
      option.textContent = lang.name;
      languageSelect.appendChild(option);
    });
    languageSelect.value = localStorage.getItem("language") || "en";
    languageSelect.addEventListener("change", () => setLanguage(languageSelect.value));
  }
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
  populateLanguageDropdown();
  updateContent();
});
  document.addEventListener("DOMContentLoaded", () => {
  const passwordInput = document.getElementById("password-input");
  const togglePassword = document.getElementById("toggle-password");
  const eyeIconOpen = document.getElementById("eye-icon-open");
  const eyeIconClosed = document.getElementById("eye-icon-closed");
  const strengthBar = document.getElementById("strength-bar");
  const strengthText = document.getElementById("strength-text");

  const requirements = [
    { id: "length", regex: /.{8,}/, score: 20 },
    { id: "lowercase", regex: /[a-z]/, score: 20 },
    { id: "uppercase", regex: /[A-Z]/, score: 20 },
    { id: "number", regex: /[0-9]/, score: 20 },
    { id: "symbol", regex: /[^A-Za-z0-9]/, score: 20 },
  ];

  const checkMarkIcon = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
    </svg>
  `;

  const xMarkIcon = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
    </svg>
  `;

  passwordInput.addEventListener("input", handlePasswordInput);
  togglePassword.addEventListener("click", togglePasswordVisibility);

  function handlePasswordInput() {
    const password = passwordInput.value;

    if (password.length === 0) {
      resetUI();
      return;
    }

    let score = 0;

    requirements.forEach((req) => {
      const reqEl = document.getElementById(req.id);
      const iconEl = reqEl.querySelector(".requirement-icon");

      if (req.regex.test(password)) {
        score += req.score;
        reqEl.classList.add("met");
        iconEl.innerHTML = checkMarkIcon;
      } else {
        reqEl.classList.remove("met");
        iconEl.innerHTML = xMarkIcon;
      }
    });

    updateStrengthUI(score);
  }

  function updateStrengthUI(score) {
    strengthBar.style.width = `${score}%`;

    if (score < 40) {
      strengthText.textContent = "Weak";
      strengthBar.style.backgroundColor = "var(--strength-weak)";
    } else if (score < 80) {
      strengthText.textContent = "Medium";
      strengthBar.style.backgroundColor = "var(--strength-medium)";
    } else {
      strengthText.textContent = score === 100 ? "Very Strong" : "Strong";
      strengthBar.style.backgroundColor =
        score === 100 ? "var(--strength-very-strong)" : "var(--strength-strong)";
    }
  }

  function resetUI() {
    strengthBar.style.width = "0%";
    strengthText.textContent = "";
    strengthBar.style.backgroundColor = "";

    requirements.forEach((req) => {
      const reqEl = document.getElementById(req.id);
      const iconEl = reqEl.querySelector(".requirement-icon");
      reqEl.classList.remove("met");
      iconEl.innerHTML = xMarkIcon;
    });
  }

  function togglePasswordVisibility() {
    const isPassword = passwordInput.type === "password";
    passwordInput.type = isPassword ? "text" : "password";
    eyeIconOpen.classList.toggle("hidden", !isPassword);
    eyeIconClosed.classList.toggle("hidden", isPassword);
  }
});

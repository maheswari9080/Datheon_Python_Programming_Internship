/**
 * Main Interactive Script for Python Internship Project Suite Portal
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Initialize Copy-to-Clipboard for Terminal Code Blocks
  const copyButtons = document.querySelectorAll(".btn-copy");

  copyButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-target");
      const targetEl = targetId ? document.getElementById(targetId) : null;
      const textToCopy = targetEl ? targetEl.innerText : btn.parentElement.nextElementSibling.innerText;

      if (navigator.clipboard && textToCopy) {
        navigator.clipboard.writeText(textToCopy.trim()).then(() => {
          const originalText = btn.innerText;
          btn.innerText = "Copied!";
          btn.style.color = "var(--success)";
          setTimeout(() => {
            btn.innerText = originalText;
            btn.style.color = "";
          }, 2000);
        });
      }
    });
  });

  // 2. Smooth scrolling for internal anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });
});

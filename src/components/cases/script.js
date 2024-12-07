document.addEventListener("DOMContentLoaded", () => {
  const sidebarPlaceholder = document.getElementById("sidebar");

  fetch("/sidebar/index.html")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to load sidebar");
      }
      return response.text();
    })
    .then((sidebarHTML) => {
      // Insert the sidebar HTML into the placeholder div
      sidebarPlaceholder.innerHTML = sidebarHTML;
    })
    .catch((error) => {
      console.error("Error loading sidebar:", error);
    });
});

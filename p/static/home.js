document.addEventListener('DOMContentLoaded', () => {
    // Get the Services toggle and parent list item
    const servicesToggle = document.querySelector('.services-toggle');
    const servicesItem = document.querySelector('.services-item');

    // Add a click event listener to the Services toggle
    servicesToggle.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent the default link behavior
        servicesItem.classList.toggle('active'); // Toggle the "active" class
    });

    // Optional: Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!servicesItem.contains(e.target) && !servicesToggle.contains(e.target)) {
            servicesItem.classList.remove('active'); // Remove "active" class if clicked outside
        }
    });

    // Toggle the navbar menu on hamburger click
    const hamburger = document.querySelector('.hamburger');
    const navbarMenu = document.querySelector('.navbar-menu');

    hamburger.addEventListener('click', () => {
        navbarMenu.classList.toggle('active'); // Toggle the navbar menu visibility
        hamburger.classList.toggle('active'); // Toggle hamburger animation (to 'X' shape)
    });

    // Handle dropdown toggle for mobile view on click
    const dropdownToggles = document.querySelectorAll('.about-toggle, .services-toggle, .contact-toggle');

    dropdownToggles.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent the default link behavior
            const dropdown = item.nextElementSibling;
            dropdown.classList.toggle('active'); // Toggle the dropdown visibility
        });
    });

    // Close the dropdown when clicking outside of the menu on mobile
    document.addEventListener('click', (e) => {
        dropdownToggles.forEach(item => {
            const dropdown = item.nextElementSibling;
            if (!item.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.classList.remove('active');
            }
        });
    });

    // Function to toggle menu
    function toggleMenu() {
        navbarMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    }

    // Toggle mobile menu visibility
    hamburger.addEventListener('click', () => {
        navbarMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('isLoggedIn'); // Remove login status
        window.location.reload(); // Reload the page to update UI
    });
});


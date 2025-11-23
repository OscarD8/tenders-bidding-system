
document.addEventListener('DOMContentLoaded', function () { // wait for document to fully load
    const toggleButton = document.querySelector('[data-collapse-toggle="navbar-sticky"]'); // trigger
    const menu = document.getElementById('navbar-sticky'); // target

    if (toggleButton && menu) { // safety check on potential null value
        toggleButton.addEventListener('click', function () {
            menu.classList.toggle('hidden'); // tailwind - if hidden remove, if not hidden add
            const isExpanded = toggleButton.getAttribute('aria-expanded') === 'true'; // accessibility
            toggleButton.setAttribute('aria-expanded', String(!isExpanded));
        });
    }
});
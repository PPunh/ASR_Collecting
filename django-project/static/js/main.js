// Custom DATA URL 
// Fixed onclick (Unexpected identifier)
document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('.row-link');
    rows.forEach(row => {
        row.addEventListener('click', function() {
            window.location.href = this.dataset.url;
        });
    });
});

// Mobile sidebar toggle (drawer + backdrop)
function toggleSidebar() {
    const sidebar = document.getElementById('mySidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    if (!sidebar) return;

    const opening = !sidebar.classList.contains('w3-show');
    sidebar.classList.toggle('w3-show', opening);
    if (backdrop) backdrop.classList.toggle('show', opening);
}

function closeSidebar() {
    const sidebar = document.getElementById('mySidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    if (sidebar) sidebar.classList.remove('w3-show');
    if (backdrop) backdrop.classList.remove('show');
}

// Close sidebar when resizing up to desktop (where it's always visible)
window.addEventListener('resize', function() {
    if (window.innerWidth >= 993) closeSidebar();
});
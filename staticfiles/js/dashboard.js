document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mainContent = document.querySelector('.main-content');

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });
    }

    if (localStorage.getItem('sidebarCollapsed') === 'true') {
        sidebar.classList.add('collapsed');
    }

    const mobileToggle = document.createElement('div');
    mobileToggle.className = 'sidebar-overlay';
    mobileToggle.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:999;display:none;';
    document.body.appendChild(mobileToggle);

    mobileToggle.addEventListener('click', function() {
        sidebar.classList.remove('active');
        this.style.display = 'none';
    });

    const mediaQuery = window.matchMedia('(max-width: 991.98px)');
    
    function handleMobileToggle() {
        if (mediaQuery.matches) {
            sidebar.classList.remove('collapsed');
            if (sidebarToggle) {
                sidebarToggle.style.display = 'none';
            }
        } else {
            sidebar.classList.remove('active');
            mobileToggle.style.display = 'none';
            if (sidebarToggle) {
                sidebarToggle.style.display = 'block';
            }
        }
    }
    
    handleMobileToggle();
    mediaQuery.addEventListener('change', handleMobileToggle);

    const searchInput = document.getElementById('searchStudent');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const tableRows = document.querySelectorAll('tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    const themeOptions = document.querySelectorAll('.theme-option');
    themeOptions.forEach(option => {
        option.addEventListener('click', function() {
            themeOptions.forEach(opt => opt.classList.remove('active'));
            this.classList.add('active');
        });
    });

    const colorOptions = document.querySelectorAll('.color-option');
    colorOptions.forEach(option => {
        option.addEventListener('click', function() {
            colorOptions.forEach(opt => opt.style.borderColor = 'transparent');
            this.style.borderColor = 'var(--primary-color)';
        });
    });

    document.querySelectorAll('.dropdown-toggle').forEach(function(dropdown) {
        new bootstrap.Dropdown(dropdown);
    });

    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });

    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} position-fixed animate-slide-in`;
        toast.style.cssText = 'top:20px;right:20px;z-index:9999;min-width:250px;';
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
            ${message}
        `;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .animate-slide-in { animation: slideIn 0.3s ease-out; }
    `;
    document.head.appendChild(style);

    document.addEventListener('click', function(e) {
        if (e.target.matches('[data-bs-toggle="tab"]')) {
            const tabId = e.target.getAttribute('href');
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('show', 'active');
            });
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            
            if (tabId) {
                const targetPane = document.querySelector(tabId);
                if (targetPane) targetPane.classList.add('show', 'active');
            }
            e.target.classList.add('active');
        }
    });

    function confirmAction(message) {
        return confirm(message);
    }

    window.confirmAction = confirmAction;

    const exportButtons = document.querySelectorAll('[data-export]');
    exportButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const type = this.getAttribute('data-export');
            console.log(`Exporting ${type}...`);
        });
    });
});

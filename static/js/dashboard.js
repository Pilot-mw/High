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
    const root = document.documentElement;
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    function applyTheme(theme) {
        root.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        if (theme === 'dark') {
            root.style.setProperty('--bg-primary', '#1a1a2e');
            root.style.setProperty('--bg-secondary', '#16213e');
            root.style.setProperty('--text-primary', '#eaeaea');
            root.style.setProperty('--text-secondary', '#a0a0a0');
            root.style.setProperty('--border-color', '#2d2d44');
        } else if (theme === 'auto') {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            applyTheme(prefersDark ? 'dark' : 'light');
            return;
        } else {
            root.style.setProperty('--bg-primary', '#ffffff');
            root.style.setProperty('--bg-secondary', '#f8f9fa');
            root.style.setProperty('--text-primary', '#212529');
            root.style.setProperty('--text-secondary', '#6c757d');
            root.style.setProperty('--border-color', '#dee2e6');
        }
    }
    
    applyTheme(savedTheme);
    
    themeOptions.forEach(option => {
        if (option.querySelector('h6').textContent.toLowerCase() === savedTheme) {
            option.classList.add('active');
        }
        option.addEventListener('click', function() {
            themeOptions.forEach(opt => opt.classList.remove('active'));
            this.classList.add('active');
            const theme = this.querySelector('h6').textContent.toLowerCase();
            applyTheme(theme);
        });
    });

    const colorOptions = document.querySelectorAll('.color-option');
    const savedPrimaryColor = localStorage.getItem('primaryColor') || '#3b82f6';
    
    function applyPrimaryColor(color) {
        document.documentElement.style.setProperty('--primary-color', color);
        localStorage.setItem('primaryColor', color);
    }
    
    applyPrimaryColor(savedPrimaryColor);
    
    colorOptions.forEach(option => {
        const rgb = getComputedStyle(option).backgroundColor;
        const hex = rgbToHex(rgb);
        if (hex.toLowerCase() === savedPrimaryColor.toLowerCase() || 
            hex.toLowerCase() === rgbToHex(savedPrimaryColor).toLowerCase()) {
            option.style.borderColor = 'var(--primary-color)';
        }
        
option.addEventListener('click', function() {
            colorOptions.forEach(opt => opt.style.borderColor = 'transparent');
            this.style.borderColor = 'var(--primary-color)';
            const clickedRgb = getComputedStyle(this).backgroundColor;
            applyPrimaryColor(clickedRgb);
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

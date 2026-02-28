
        // Theme Management
        // Theme Management
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        
        function setTheme(theme) {
            document.documentElement.setAttribute('data-bs-theme', theme);
            localStorage.setItem('theme', theme);
            
            if (themeIcon) {
                if (theme === 'dark') {
                    themeIcon.className = 'bi bi-moon-fill';
                } else {
                    themeIcon.className = 'bi bi-sun-fill';
                }
            }
        }

        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        }

        // Initialize theme
        const savedTheme = localStorage.getItem('theme') || 'light';
        setTheme(savedTheme);

        if (themeToggle) {
            themeToggle.addEventListener('click', toggleTheme);
        }

        // Mobile sidebar toggle
        const sidebarToggle = document.getElementById('sidebarToggle');
        const sidebar = document.getElementById('sidebar');
        
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => {
                sidebar.classList.toggle('show');
            });
        }

        // Update current date and time
        function updateDateTime() {
            const now = new Date();
            const options = {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            };
            
            const dateTimeElement = document.getElementById('currentDateTime');
            if (dateTimeElement) {
                dateTimeElement.textContent = now.toLocaleDateString('ar-SA', options);
            }
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            updateDateTime();
            setInterval(updateDateTime, 60000); // Update every minute
        });

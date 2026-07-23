/**
 * Vulnerable Lab - Enhanced JavaScript
 * Adds interactivity and visual enhancements
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔐 Vulnerable Lab loaded successfully!');
    
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltips.length) {
        tooltips.forEach(t => new bootstrap.Tooltip(t));
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Command history for ping page
    const commandInput = document.getElementById('ip');
    const quickButtons = document.querySelectorAll('[onclick^="insertCommand"]');
    
    quickButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            if (commandInput) {
                commandInput.focus();
                commandInput.setSelectionRange(commandInput.value.length, commandInput.value.length);
            }
        });
    });
    
    // Keyboard shortcut: Ctrl+Enter to submit forms
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                if (form.contains(document.activeElement)) {
                    form.submit();
                }
            });
        }
    });
    
    // Copy code snippets on click
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        block.addEventListener('click', function() {
            const text = this.textContent;
            navigator.clipboard.writeText(text).then(() => {
                // Show a small feedback
                const original = this.style.borderColor;
                this.style.borderColor = '#00D2A0';
                setTimeout(() => {
                    this.style.borderColor = original;
                }, 1000);
            }).catch(() => {});
        });
    });
    
    // Animate stats on scroll
    const statNumbers = document.querySelectorAll('.stat-number');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const text = el.textContent;
                if (!isNaN(text)) {
                    const num = parseInt(text);
                    let current = 0;
                    const increment = Math.ceil(num / 30);
                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= num) {
                            current = num;
                            clearInterval(timer);
                        }
                        el.textContent = current;
                    }, 50);
                }
            }
        });
    });
    
    statNumbers.forEach(num => observer.observe(num));
    
    // Add a subtle glow effect to navbar brand on hover
    const brand = document.querySelector('.navbar-brand');
    if (brand) {
        brand.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.3s ease';
        });
        brand.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    }
    
    // File input label update
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const label = this.nextElementSibling;
            if (label && label.classList.contains('form-label')) {
                if (this.files.length) {
                    label.textContent = this.files[0].name;
                } else {
                    label.textContent = 'Choose file';
                }
            }
        });
    }
    
    // Add loading state to buttons on submit
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitBtn.disabled = true;
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
    
    // Generate report button functionality
    const reportBtn = document.getElementById('generateReportBtn');
    if (reportBtn) {
        reportBtn.addEventListener('click', function() {
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
            this.disabled = true;
            
            fetch('/generate_report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = data.download_url;
                } else {
                    alert('Error generating report: ' + data.error);
                }
            })
            .catch(error => {
                alert('Error: ' + error);
            })
            .finally(() => {
                this.innerHTML = '<i class="fas fa-file-alt"></i> Generate Report';
                this.disabled = false;
            });
        });
    }
});

/**
 * Utility function to insert a command into the ping input
 */
function insertCommand(cmd) {
    const input = document.getElementById('ip');
    if (input) {
        input.value = cmd;
        input.focus();
    }
}

/**
 * Utility function to copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show a toast or something
        console.log('Copied to clipboard!');
    }).catch(() => {});
}

/**
 * Utility function to toggle dark/light mode (if needed)
 */
function toggleTheme() {
    document.body.classList.toggle('light-mode');
    const icon = document.querySelector('#themeToggle i');
    if (icon) {
        icon.classList.toggle('fa-moon');
        icon.classList.toggle('fa-sun');
    }
}

console.log('✨ Vulnerable Lab scripts loaded!');
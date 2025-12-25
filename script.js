// ===================================
// Loading Screen
// ===================================
function handleLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');

    // Hide loading screen after page loads
    window.addEventListener('load', () => {
        setTimeout(() => {
            loadingScreen.classList.add('hidden');
        }, 500); // Small delay for smooth transition
    });
}

// ===================================
// Scroll Animations
// ===================================
function animateOnScroll() {
    const elements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    elements.forEach(element => observer.observe(element));
}

// ===================================
// Navbar Scroll Effect
// ===================================
function handleNavbarScroll() {
    const navbar = document.getElementById('navbar');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// ===================================
// Counter Animation
// ===================================
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-target'));
                const duration = 2000; // 2 seconds
                const increment = target / (duration / 16); // 60fps
                let current = 0;

                const updateCounter = () => {
                    current += increment;
                    if (current < target) {
                        entry.target.textContent = Math.floor(current).toLocaleString();
                        requestAnimationFrame(updateCounter);
                    } else {
                        // Add special formatting for specific counters
                        const parent = entry.target.closest('.stat-item');
                        const label = parent.querySelector('.stat-label').textContent;

                        if (label.includes('Satisfaction')) {
                            entry.target.textContent = target + '%';
                        } else if (label.includes('Support')) {
                            entry.target.textContent = target + '/7';
                        } else {
                            entry.target.textContent = target.toLocaleString() + '+';
                        }
                    }
                };

                updateCounter();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

// ===================================
// Mobile Menu Toggle
// ===================================
function setupMobileMenu() {
    const mobileToggle = document.getElementById('mobile-toggle');
    const navLinks = document.querySelector('.nav-links');

    mobileToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileToggle.classList.toggle('active');
    });

    // Close menu when clicking on a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            mobileToggle.classList.remove('active');
        });
    });
}

// ===================================
// Smooth Scroll for Navigation Links
// ===================================
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));

            if (target) {
                const navbarHeight = document.getElementById('navbar').offsetHeight;
                const targetPosition = target.offsetTop - navbarHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===================================
// Contact Form Handling
// ===================================
function setupContactForm() {
    const form = document.getElementById('contact-form');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // Get form values
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        // Here you would typically send the data to a server
        // For this template, we'll just show an alert
        alert(`Thank you ${name}! We'll get back to you at ${email} soon.`);

        // Reset form
        form.reset();
    });
}

// ===================================
// Parallax Effect for Hero Orbs
// ===================================
function setupParallax() {
    const orbs = document.querySelectorAll('.gradient-orb');

    window.addEventListener('mousemove', (e) => {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;

        orbs.forEach((orb, index) => {
            const speed = (index + 1) * 20;
            const x = (mouseX - 0.5) * speed;
            const y = (mouseY - 0.5) * speed;

            orb.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
        });
    });
}

// ===================================
// Feature Card Tilt Effect
// ===================================
function setupCardTilt() {
    const cards = document.querySelectorAll('.feature-card, .testimonial-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });
}

// ===================================
// CTA Button Ripple Effect
// ===================================
function setupRippleEffect() {
    const buttons = document.querySelectorAll('.btn, .cta-button');

    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            // Add ripple styles dynamically
            if (!document.getElementById('ripple-styles')) {
                const style = document.createElement('style');
                style.id = 'ripple-styles';
                style.textContent = `
                    .ripple {
                        position: absolute;
                        border-radius: 50%;
                        background: rgba(255, 255, 255, 0.3);
                        transform: scale(0);
                        animation: ripple-animation 0.6s ease-out;
                        pointer-events: none;
                    }
                    @keyframes ripple-animation {
                        to {
                            transform: scale(4);
                            opacity: 0;
                        }
                    }
                    .btn, .cta-button {
                        position: relative;
                        overflow: hidden;
                    }
                `;
                document.head.appendChild(style);
            }

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });
}

// ===================================
// Typing Effect for Hero Title (Optional)
// ===================================
function setupTypingEffect() {
    const heroTitle = document.querySelector('.hero-title');
    if (!heroTitle) return;

    const text = heroTitle.innerHTML;
    heroTitle.innerHTML = '';
    heroTitle.style.opacity = '1';

    let index = 0;
    const speed = 50;

    function type() {
        if (index < text.length) {
            heroTitle.innerHTML += text.charAt(index);
            index++;
            setTimeout(type, speed);
        }
    }

    // Uncomment to enable typing effect
    // type();
}

// ===================================
// Initialize All Features
// ===================================
document.addEventListener('DOMContentLoaded', () => {
    handleLoadingScreen();
    animateOnScroll();
    handleNavbarScroll();
    animateCounters();
    setupMobileMenu();
    setupSmoothScroll();
    setupContactForm();
    setupParallax();
    setupCardTilt();
    setupRippleEffect();
    // setupTypingEffect(); // Optional: Uncomment to enable

    // Add a small delay before showing animations for better UX
    setTimeout(() => {
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            if (el.getBoundingClientRect().top < window.innerHeight) {
                el.classList.add('visible');
            }
        });
    }, 100);
});

// ===================================
// Performance Optimization
// ===================================
// Debounce function for scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimize scroll events
window.addEventListener('scroll', debounce(() => {
    // Additional scroll-based animations can be added here
}, 10));

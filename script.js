// ===================================
// Loading Screen
// ===================================
function handleLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    
    // Animate brand name letters if they exist
    const brandName = document.querySelector('.loading-brand');
    if (brandName && !brandName.querySelector('span')) {
        // If the span structure isn't there, we rely on the CSS animation 
        // working on the existing structure or the replacement we make in html
    }

    // Hide loading screen after page loads
    window.addEventListener('load', () => {
        setTimeout(() => {
            loadingScreen.classList.add('hidden');
            // Trigger initial animations after loader is gone
            setTimeout(triggerInitialAnimations, 500);
        }, 1500); // Extended delay for users to see the nice animation
    });
}

function triggerInitialAnimations() {
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        if (el.getBoundingClientRect().top < window.innerHeight) {
            el.classList.add('visible');
        }
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

    elements.forEach(element => {
        // Default to fade-up if no specific animation class is present
        if (!element.classList.contains('fade-left') && 
            !element.classList.contains('fade-right') && 
            !element.classList.contains('scale-in')) {
            element.classList.add('fade-up');
        }
        observer.observe(element);
    });
}

// ===================================
// Modern Carousel
// ===================================
function setupCarousel() {
    const carousels = document.querySelectorAll('.carousel-container');
    
    carousels.forEach(container => {
        const track = container.querySelector('.carousel-track');
        if (!track) return;

        const slides = Array.from(track.children);
        const nextButton = container.querySelector('.carousel-nav.next');
        const prevButton = container.querySelector('.carousel-nav.prev');
        const indicatorsContainer = container.querySelector('.carousel-indicators');
        
        let slideWidth = slides[0].getBoundingClientRect().width;
        let currentSlideIndex = 0;
        let autoplayInterval;

        // Position slides
        const setSlidePosition = (slide, index) => {
            slide.style.left = slideWidth * index + 'px';
        };
        // We actually want them relative in flex, so we might not need absolute positioning logic
        // But for a sliding track, we usually move the track. Let's stick to track translation.
        
        const updateSlideWidth = () => {
            slideWidth = slides[0].getBoundingClientRect().width;
            moveToSlide(currentSlideIndex);
        };

        const moveToSlide = (index) => {
            track.style.transform = 'translateX(-' + (slideWidth * index) + 'px)';
            currentSlideIndex = index;
            
            // Update active classes
            slides.forEach(slide => slide.classList.remove('active'));
            slides[index].classList.add('active');
            
            updateIndicators(index);
        };

        const updateIndicators = (index) => {
            if (!indicatorsContainer) return;
            const indicators = Array.from(indicatorsContainer.children);
            indicators.forEach(ind => ind.classList.remove('active'));
            if (indicators[index]) indicators[index].classList.add('active');
        };

        // Create indicators
        if (indicatorsContainer) {
            slides.forEach((_, i) => {
                const indicator = document.createElement('div');
                indicator.classList.add('indicator');
                if (i === 0) indicator.classList.add('active');
                indicator.addEventListener('click', () => {
                    moveToSlide(i);
                    resetAutoplay();
                });
                indicatorsContainer.appendChild(indicator);
            });
        }

        // Navigation Events
        if (nextButton) {
            nextButton.addEventListener('click', () => {
                const nextIndex = (currentSlideIndex + 1) % slides.length;
                moveToSlide(nextIndex);
                resetAutoplay();
            });
        }

        if (prevButton) {
            prevButton.addEventListener('click', () => {
                const prevIndex = (currentSlideIndex - 1 + slides.length) % slides.length;
                moveToSlide(prevIndex);
                resetAutoplay();
            });
        }

        // Autoplay
        const startAutoplay = () => {
            autoplayInterval = setInterval(() => {
                const nextIndex = (currentSlideIndex + 1) % slides.length;
                moveToSlide(nextIndex);
            }, 5000);
        };

        const stopAutoplay = () => {
            clearInterval(autoplayInterval);
        };

        const resetAutoplay = () => {
            stopAutoplay();
            startAutoplay();
        };

        // Initialize
        window.addEventListener('resize', updateSlideWidth);
        slides[0].classList.add('active');
        startAutoplay();
        
        // Pause on hover
        container.addEventListener('mouseenter', stopAutoplay);
        container.addEventListener('mouseleave', startAutoplay);
    });
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
                const duration = 2000;
                const increment = target / (duration / 16);
                let current = 0;
                
                const updateCounter = () => {
                    current += increment;
                    if (current < target) {
                        entry.target.textContent = Math.floor(current).toLocaleString();
                        requestAnimationFrame(updateCounter);
                    } else {
                        // Formatting logic preserved
                        const parent = entry.target.closest('.stat-item');
                        const label = parent ? parent.querySelector('.stat-label').textContent : '';
                        
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
    
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileToggle.classList.toggle('active');
        });

        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileToggle.classList.remove('active');
            });
        });
    }
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
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        
        alert(`Thank you ${name}! We'll get back to you at ${email} soon.`);
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
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size/2;
            const y = e.clientY - rect.top - size/2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            // Add ripple styles logic if not present (handled better in CSS usually, but preserving logic)
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
                        to { transform: scale(4); opacity: 0; }
                    }
                    .btn, .cta-button { position: relative; overflow: hidden; }
                `;
                document.head.appendChild(style);
            }
            
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
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
    setupCarousel(); // Initialize the new carousel
});

// ===================================
// Performance Optimization
// ===================================
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

window.addEventListener('scroll', debounce(() => {
    // Optional scroll logic
}, 10));

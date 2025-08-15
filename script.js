document.addEventListener("DOMContentLoaded", function() {

    // 1. Membuat header memiliki background saat di-scroll
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // 2. Intersection Observer untuk animasi scroll
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Ambil semua elemen content-section yang ingin dianimasikan
    const sectionsToAnimate = document.querySelectorAll('.content-section');
    sectionsToAnimate.forEach(section => {
        section.classList.add('fade-in-element');
        observer.observe(section);
    });

});
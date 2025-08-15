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

    // 2. Animasi Fade-in saat elemen terlihat di layar
    const observerOptions = {
        root: null, // viewport
        rootMargin: '0px',
        threshold: 0.1 // elemen dianggap terlihat jika 10% areanya masuk viewport
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Hentikan observasi setelah animasi berjalan
            }
        });
    }, observerOptions);

    // Ambil semua elemen yang ingin dianimasikan
    const sectionsToAnimate = document.querySelectorAll('.content-section, .project-card');
    sectionsToAnimate.forEach(section => {
        section.classList.add('fade-in-element'); // Tambahkan class awal
        observer.observe(section);
    });

});
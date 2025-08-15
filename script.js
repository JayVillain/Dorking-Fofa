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

    // Ambil semua elemen umum yang ingin dianimasikan
    const sectionsToAnimate = document.querySelectorAll('.content-section');
    sectionsToAnimate.forEach(section => {
        section.classList.add('fade-in-element');
        observer.observe(section);
    });

    // Logika Khusus untuk Efek Stagger (berurutan) pada Kartu Proyek
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach((card, index) => {
        card.classList.add('fade-in-element');
        // Berikan delay yang berbeda untuk setiap kartu berdasarkan urutannya
        card.style.transitionDelay = `${index * 150}ms`; 
        observer.observe(card);
    });

});
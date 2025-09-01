let lightbox = document.getElementById('lightbox');
let lightboxImg = document.getElementById('lightbox-img');
let startX = 0;

function openLightbox(src) {
    lightbox.style.display = 'flex';
    lightboxImg.src = src;
}

function closeLightbox() {
    lightbox.style.display = 'none';
    lightboxImg.src = '';
}

// Swipe para volver a la página principal
lightbox.addEventListener('touchstart', e => {
    startX = e.touches[0].clientX;
});

lightbox.addEventListener('touchend', e => {
    let endX = e.changedTouches[0].clientX;
    if (endX - startX > 50) {  // swipe derecha
        window.history.back();
    }
});

document.getElementById('lightbox').addEventListener('click', e => {
    if (e.target.id === 'lightbox' || e.target.classList.contains('close')) {
        closeLightbox();
    }
});

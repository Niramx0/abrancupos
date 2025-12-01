const scroller = document.querySelector('.info-scroller');
const thumb = document.querySelector('.scroll-thumb');
const track = document.querySelector('.scroll-track');

// 2. Función que actualiza la posición del pulgar
function updateScrollThumb() {
    const scrollDistance = scroller.scrollWidth - scroller.clientWidth;
    
    if (scrollDistance <= 0) { 
        // Si no hay scroll, posiciona el pulgar al inicio.
        thumb.style.left = '1px'; 
        return;
    }

    const scrollPercentage = scroller.scrollLeft / scrollDistance;
    
    // Ancho total disponible para el movimiento del pulgar (Track width - Thumb width - pequeños márgenes)
    const availableTrackWidth = track.clientWidth - thumb.clientWidth - 2; 
    
    // Calcular la nueva posición 'left' (ajustando por el margen/borde de 1px)
    const newLeft = (scrollPercentage * availableTrackWidth) + 1; 

    // Aplicar la nueva posición
    thumb.style.left = `${newLeft}px`;
}

// 3. Event Listeners: Ejecutar la función cuando el usuario hace scroll o cuando la ventana cambia de tamaño
scroller.addEventListener('scroll', updateScrollThumb);
window.addEventListener('load', updateScrollThumb);
window.addEventListener('resize', updateScrollThumb);
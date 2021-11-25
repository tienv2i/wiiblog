// import 'tailwindcss';
import './style.scss';
import Alpine from 'alpinejs';

window.Alpine = Alpine;
queueMicrotask(() => {
    Alpine.start();
});


function toggle (selector) {
    let els = document.querySelectorAll(selector);
    Array.prototype.map.call(els, (el) => {
        el.classList.contains('hidden') ? el.classList.remove('hidden') : el.classList.add('hidden');
    })
}
window.toggle = toggle;
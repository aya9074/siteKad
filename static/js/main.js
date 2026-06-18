document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // ========================================
    // БОКОВАЯ ПАНЕЛЬ (гамбургер)
    // ========================================
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarClose = document.querySelector('.sidebar-close');
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);
    
    function openSidebar() {
        sidebar.classList.add('open');
        menuToggle.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    function closeSidebar() {
        sidebar.classList.remove('open');
        menuToggle.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            if (sidebar.classList.contains('open')) {
                closeSidebar();
            } else {
                openSidebar();
            }
        });
    }
    
    if (sidebarClose) {
        sidebarClose.addEventListener('click', closeSidebar);
    }
    
    overlay.addEventListener('click', closeSidebar);
    
    // Закрываем по Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('open')) {
            closeSidebar();
        }
    });
    
    // ========================================
    // СКРЫТИЕ ВЕРХНЕЙ ПЛАШКИ ПРИ СКРОЛЛЕ
    // ========================================
    const header = document.querySelector('.header');
    let lastScrollY = window.scrollY;
    let ticking = false;
    
    function handleScroll() {
        if (!header) return;
        
        const currentScrollY = window.scrollY;
        
        // Если скроллим вниз и не в самом верху - скрываем
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            header.classList.add('hidden');
        } 
        // Если скроллим вверх - показываем
        else if (currentScrollY < lastScrollY) {
            header.classList.remove('hidden');
        }
        
        // Если мы в самом верху - показываем всегда
        if (currentScrollY < 50) {
            header.classList.remove('hidden');
        }
        
        lastScrollY = currentScrollY;
        ticking = false;
    }
    
    window.addEventListener('scroll', function() {
        if (!ticking) {
            window.requestAnimationFrame(function() {
                handleScroll();
                ticking = false;
            });
            ticking = true;
        }
    });
    
    // ========================================
    // АКТИВНЫЙ ПУНКТ МЕНЮ (подсветка текущей страницы)
    // ========================================
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.sidebar-menu a');
    
    menuLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.style.background = 'rgba(255, 255, 255, 0.15)';
            link.style.fontWeight = 'bold';
        }
    });
    
    // ========================================
    // ПЛАВНАЯ ЗАГРУЗКА СТРАНИЦЫ
    // ========================================
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.3s ease';
    
    window.addEventListener('load', function() {
        document.body.style.opacity = '1';
    });
});

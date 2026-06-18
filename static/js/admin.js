document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // ========================================
    // ПОДТВЕРЖДЕНИЕ УДАЛЕНИЯ
    // ========================================
    const deleteButtons = document.querySelectorAll('.btn-delete');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const confirmMessage = this.getAttribute('data-confirm') || 'Вы уверены, что хотите удалить этот элемент?';
            if (!confirm(confirmMessage)) {
                e.preventDefault();
            }
        });
    });
    
    // ========================================
    // АВТОМАТИЧЕСКОЕ СКРЫТИЕ FLASH-СООБЩЕНИЙ
    // ========================================
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 500);
        }, 4000);
    });
    
    // ========================================
    // ВАЛИДАЦИЯ ФОРМ (базовая)
    // ========================================
    const forms = document.querySelectorAll('.admin-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#e74c3c';
                    isValid = false;
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Пожалуйста, заполните все обязательные поля (отмечены *)');
            }
        });
    });
    
    // ========================================
    // ПРЕДПРОСМОТР ФОТО ПРИ ЗАГРУЗКЕ
    // ========================================
    const photoInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    photoInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                const previewContainer = this.parentElement.querySelector('.photo-preview');
                
                reader.onload = function(e) {
                    if (previewContainer) {
                        previewContainer.innerHTML = `
                            <img src="${e.target.result}" alt="Предпросмотр" style="max-width: 200px; border-radius: 8px; margin-top: 10px;">
                        `;
                    }
                };
                
                reader.readAsDataURL(file);
            }
        });
    });
});

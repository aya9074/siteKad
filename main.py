from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import json

from config import Config
from models import db, User, Setting, Page, MenuItem

# ============================================
# Инициализация приложения
# ============================================
app = Flask(__name__)
app.config.from_object(Config)

# ============================================
# База данных (инициализируем с app)
# ============================================
db.init_app(app)

# ============================================
# Авторизация
# ============================================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin.login'
login_manager.login_message = 'Пожалуйста, авторизуйтесь для доступа к админ-панели'
login_manager.login_message_category = 'warning'

# ============================================
# Регистрируем Blueprint админки
# ============================================
from admin.routes import admin_bp
app.register_blueprint(admin_bp)

# ============================================
# Загрузка пользователя
# ============================================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============================================
# Инициализация БД (при первом запуске)
# ============================================
def init_db():
    """Создает таблицы и первого администратора"""
    with app.app_context():
        db.create_all()
        
        # Проверяем, есть ли пользователь
        if not User.query.first():
            admin = User(username=app.config['ADMIN_USERNAME'])
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            db.session.commit()
            print(f'✅ Создан администратор: {app.config["ADMIN_USERNAME"]}')
        
        # Создаем настройки по умолчанию
        default_settings = {
            'site_name': 'Абсолют Кадастр',
            'site_description': 'Профессиональные кадастровые услуги в Тамбове',
            'contact_phone': '+7 (4752) XX-XX-XX',
            'contact_email': 'info@absolut-kadastr.ru',
            'contact_address': 'г. Тамбов, ул. Примерная, д. 1',
            'social_vk': 'https://vk.com/absolutkadastr',
            'social_telegram': 'https://t.me/absolutkadastr',
            'social_whatsapp': 'https://wa.me/79001234567',
            'accreditation_text': 'Лицензия № XX-XX-XX-XX',
        }
        
        for key, value in default_settings.items():
            if not Setting.query.filter_by(key=key).first():
                db.session.add(Setting(key=key, value=value))
        
        db.session.commit()
        print('✅ Созданы настройки по умолчанию')

# ============================================
# ОБРАБОТЧИКИ ОШИБОК
# ============================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# ============================================
# МАРШРУТЫ КЛИЕНТСКОЙ ЧАСТИ
# ============================================

@app.route('/')
def index():
    """Главная страница"""
    # Получаем настройки для отображения в шаблоне
    settings = {
        'site_name': Setting.get('site_name', 'Абсолют Кадастр'),
        'site_description': Setting.get('site_description', ''),
        'contact_phone': Setting.get('contact_phone', ''),
        'contact_email': Setting.get('contact_email', ''),
        'contact_address': Setting.get('contact_address', ''),
        'social_vk': Setting.get('social_vk', ''),
        'social_telegram': Setting.get('social_telegram', ''),
        'social_whatsapp': Setting.get('social_whatsapp', ''),
        'accreditation_text': Setting.get('accreditation_text', ''),
    }
    return render_template('index.html', **settings)


@app.route('/page/<slug>')
def page_detail(slug):
    """Страница по slug"""
    page = Page.query.filter_by(slug=slug, is_published=True).first_or_404()
    
    # Получаем настройки для отображения в шаблоне
    settings = {
        'site_name': Setting.get('site_name', 'Абсолют Кадастр'),
        'contact_phone': Setting.get('contact_phone', ''),
        'contact_email': Setting.get('contact_email', ''),
        'contact_address': Setting.get('contact_address', ''),
        'social_vk': Setting.get('social_vk', ''),
        'social_telegram': Setting.get('social_telegram', ''),
        'social_whatsapp': Setting.get('social_whatsapp', ''),
        'accreditation_text': Setting.get('accreditation_text', ''),
    }
    return render_template('page.html', page=page, **settings)


# ============================================
# ЗАПУСК
# ============================================

if __name__ == '__main__':
    init_db()
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
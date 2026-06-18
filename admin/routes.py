from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user

from . import admin_bp
from models import db, User
from core.page_manager import PageManager
from core.menu_manager import MenuManager
from core.upload_manager import UploadManager

# ============================================
# АВТОРИЗАЦИЯ
# ============================================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Неверный логин или пароль', 'danger')
    
    return render_template('login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    """Выход из админки"""
    logout_user()
    flash('Вы вышли из админки', 'info')
    return redirect(url_for('admin.login'))


# ============================================
# ДАШБОРД
# ============================================

@admin_bp.route('/')
@login_required
def dashboard():
    """Главная страница админки"""
    return render_template('dashboard.html')


# ============================================
# УПРАВЛЕНИЕ СТРАНИЦАМИ (только маршруты)
# ============================================

@admin_bp.route('/pages')
@login_required
def pages():
    """Список страниц"""
    pages_list = PageManager.get_all()
    return render_template('pages_list.html', pages=pages_list)


@admin_bp.route('/page/new', methods=['GET', 'POST'])
@login_required
def page_new():
    """Создание страницы"""
    if request.method == 'POST':
        PageManager.create(request.form)
        flash('Страница создана!', 'success')
        return redirect(url_for('admin.pages'))
    
    return render_template('page_edit.html', page=None)


@admin_bp.route('/page/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def page_edit(id):
    """Редактирование страницы"""
    if request.method == 'POST':
        PageManager.update(id, request.form)
        flash('Страница обновлена!', 'success')
        return redirect(url_for('admin.pages'))
    
    page = PageManager.get_by_id(id)
    return render_template('page_edit.html', page=page)


@admin_bp.route('/page/delete/<int:id>')
@login_required
def page_delete(id):
    """Удаление страницы"""
    PageManager.delete(id)
    flash('Страница удалена', 'warning')
    return redirect(url_for('admin.pages'))


@admin_bp.route('/page/delete_photo/<int:id>')
@login_required
def page_delete_photo(id):
    """Удаление фото страницы"""
    PageManager.delete_photo(id)
    flash('Фото удалено', 'info')
    return redirect(url_for('admin.page_edit', id=id))


# ============================================
# УПРАВЛЕНИЕ МЕНЮ (только маршруты)
# ============================================

@admin_bp.route('/menu')
@login_required
def menu():
    """Управление меню"""
    items = MenuManager.get_all()
    return render_template('menu_edit.html', menu_items=items)


@admin_bp.route('/menu/move/<int:id>/<direction>')
@login_required
def menu_move(id, direction):
    """Перемещение пункта меню"""
    if direction == 'up':
        MenuManager.move_up(id)
    elif direction == 'down':
        MenuManager.move_down(id)
    flash('Порядок изменен', 'info')
    return redirect(url_for('admin.menu'))
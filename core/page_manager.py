from models import db, Page
from werkzeug.utils import secure_filename
import os
from config import Config

class PageManager:
    """Управление страницами - вся логика здесь"""
    
    @staticmethod
    def get_all():
        """Получить все страницы"""
        return Page.query.order_by(Page.updated_at.desc()).all()
    
    @staticmethod
    def get_by_id(page_id):
        """Получить страницу по ID"""
        return Page.query.get_or_404(page_id)
    
    @staticmethod
    def get_by_slug(slug):
        """Получить страницу по slug"""
        return Page.query.filter_by(slug=slug, is_published=True).first_or_404()
    
    @staticmethod
    def create(data):
        """Создать страницу"""
        page = Page(
            slug=data.get('slug'),
            title=data.get('title'),
            content=data.get('content'),
            has_photo='has_photo' in data,
            has_map='has_map' in data,
            map_coords=data.get('map_coords'),
            map_zoom=data.get('map_zoom', 15),
            is_published='is_published' in data
        )
        db.session.add(page)
        db.session.commit()
        return page
    
    @staticmethod
    def update(page_id, data):
        """Обновить страницу"""
        page = Page.query.get_or_404(page_id)
        page.slug = data.get('slug')
        page.title = data.get('title')
        page.content = data.get('content')
        page.has_photo = 'has_photo' in data
        page.has_map = 'has_map' in data
        page.map_coords = data.get('map_coords')
        page.map_zoom = data.get('map_zoom', 15)
        page.is_published = 'is_published' in data
        db.session.commit()
        return page
    
    @staticmethod
    def delete(page_id):
        """Удалить страницу"""
        page = Page.query.get_or_404(page_id)
        db.session.delete(page)
        db.session.commit()
    
    @staticmethod
    def delete_photo(page_id):
        """Удалить фото страницы"""
        page = Page.query.get_or_404(page_id)
        if page.photo_path:
            try:
                os.remove(os.path.join(Config.UPLOAD_FOLDER, page.photo_path))
            except:
                pass
            page.photo_path = None
            page.has_photo = False
            db.session.commit()

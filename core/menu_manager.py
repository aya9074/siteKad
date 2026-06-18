
from models import db, MenuItem

class MenuManager:
    """Управление меню - вся логика здесь"""
    
    @staticmethod
    def get_all():
        """Получить все пункты меню"""
        return MenuItem.query.order_by(MenuItem.sort_order).all()
    
    @staticmethod
    def get_by_id(item_id):
        """Получить пункт меню по ID"""
        return MenuItem.query.get_or_404(item_id)
    
    @staticmethod
    def create(data):
        """Создать пункт меню"""
        item = MenuItem(
            title=data.get('title'),
            parent_id=data.get('parent_id'),
            page_id=data.get('page_id'),
            url=data.get('url'),
            sort_order=data.get('sort_order', 0),
            is_visible='is_visible' in data
        )
        db.session.add(item)
        db.session.commit()
        return item
    
    @staticmethod
    def update(item_id, data):
        """Обновить пункт меню"""
        item = MenuItem.query.get_or_404(item_id)
        item.title = data.get('title')
        item.parent_id = data.get('parent_id')
        item.page_id = data.get('page_id')
        item.url = data.get('url')
        item.sort_order = data.get('sort_order', 0)
        item.is_visible = 'is_visible' in data
        db.session.commit()
        return item
    
    @staticmethod
    def delete(item_id):
        """Удалить пункт меню"""
        item = MenuItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
    
    @staticmethod
    def move_up(item_id):
        """Переместить пункт меню вверх"""
        item = MenuItem.query.get_or_404(item_id)
        prev = MenuItem.query.filter(
            MenuItem.sort_order < item.sort_order,
            MenuItem.parent_id == item.parent_id
        ).order_by(MenuItem.sort_order.desc()).first()
        
        if prev:
            item.sort_order, prev.sort_order = prev.sort_order, item.sort_order
            db.session.commit()
    
    @staticmethod
    def move_down(item_id):
        """Переместить пункт меню вниз"""
        item = MenuItem.query.get_or_404(item_id)
        next_item = MenuItem.query.filter(
            MenuItem.sort_order > item.sort_order,
            MenuItem.parent_id == item.parent_id
        ).order_by(MenuItem.sort_order.asc()).first()
        
        if next_item:
            item.sort_order, next_item.sort_order = next_item.sort_order, item.sort_order
            db.session.commit()
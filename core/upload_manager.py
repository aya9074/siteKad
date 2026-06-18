import os
from werkzeug.utils import secure_filename
from datetime import datetime
from config import Config

class UploadManager:
    """Управление загрузкой файлов - вся логика здесь"""
    
    @staticmethod
    def allowed_file(filename):
        """Проверка разрешенного расширения"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    
    @staticmethod
    def save_photo(file, subfolder='pages'):
        """Сохранить фото и вернуть путь"""
        if not file or file.filename == '':
            return None
        
        if not UploadManager.allowed_file(file.filename):
            return None
        
        filename = secure_filename(file.filename)
        # Добавляем временную метку, чтобы избежать конфликтов
        name, ext = filename.rsplit('.', 1)
        filename = f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        
        # Создаем папку если её нет
        upload_path = os.path.join(Config.UPLOAD_FOLDER, subfolder)
        os.makedirs(upload_path, exist_ok=True)
        
        # Сохраняем файл
        file_path = os.path.join(subfolder, filename)
        full_path = os.path.join(Config.UPLOAD_FOLDER, file_path)
        file.save(full_path)
        
        return file_path
    
    @staticmethod
    def delete_file(file_path):
        """Удалить файл"""
        if file_path:
            try:
                full_path = os.path.join(Config.UPLOAD_FOLDER, file_path)
                if os.path.exists(full_path):
                    os.remove(full_path)
                    return True
            except:
                pass
        return False

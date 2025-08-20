from mongoengine import connect
from flask import g
from models import Province, Attraction

db = None

def init_db(app):
    # 初始化MongoDB连接
    global db
    db = connect(
        db=app.config.get('MONGODB_SETTINGS', {}).get('db', 'virtual_tourism'),
        host=app.config.get('MONGODB_SETTINGS', {}).get('host', 'localhost'),
        port=app.config.get('MONGODB_SETTINGS', {}).get('port', 27017)
    )
    
    # 在应用上下文中存储数据库连接
    @app.before_request
    def before_request():
        g.db = db
        
    return db
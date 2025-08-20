from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from config import Config
from database import init_db
from routes import init_routes
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 添加错误处理
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({"error": "Internal server error", "message": str(error)}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        logger.error(f"Resource not found: {error}")
        return jsonify({"error": "Resource not found"}), 404
    
    # 初始化数据库
    try:
        init_db(app)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise e
    
    # 启用CORS
    CORS(app)
    
    # 创建API实例
    api = Api(app)
    
    # 初始化路由
    try:
        init_routes(api)
        logger.info("Routes initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize routes: {e}")
        raise e
    
    @app.route('/')
    def index():
        return jsonify({
            "message": "欢迎使用云旅游API",
            "version": "1.0"
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
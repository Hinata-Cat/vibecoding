from flask_restful import Resource
from models import Province, Attraction
from flask import request, g
import logging

# 配置日志
logger = logging.getLogger(__name__)

class ProvinceListResource(Resource):
    def get(self):
        """获取所有省份列表"""
        try:
            provinces = Province.objects.all()
            return [province.to_dict() for province in provinces], 200
        except Exception as e:
            logger.error(f"Error fetching provinces: {e}")
            return {'error': 'Failed to fetch provinces', 'message': str(e)}, 500

class ProvinceResource(Resource):
    def get(self, province_id):
        """获取特定省份信息"""
        try:
            province = Province.objects(id=province_id).first()
            if not province:
                return {'error': 'Province not found'}, 404
            return province.to_dict(), 200
        except Exception as e:
            logger.error(f"Error fetching province {province_id}: {e}")
            return {'error': 'Failed to fetch province', 'message': str(e)}, 500

class ProvinceByNameResource(Resource):
    def get(self, province_name):
        """根据省份名称获取省份信息"""
        try:
            # 处理URL编码的省份名称
            import urllib.parse
            province_name = urllib.parse.unquote(province_name)
            
            province = Province.objects(name=province_name).first()
            if not province:
                return {'error': 'Province not found'}, 404
            return province.to_dict(), 200
        except Exception as e:
            logger.error(f"Error fetching province {province_name}: {e}")
            return {'error': 'Failed to fetch province', 'message': str(e)}, 500

class AttractionListResource(Resource):
    def get(self):
        """获取所有景点列表，可按省份筛选"""
        try:
            province_id = request.args.get('province_id')
            province_name = request.args.get('province_name')
            
            if province_id:
                try:
                    # 验证province_id是否有效
                    province = Province.objects(id=province_id).first()
                    if not province:
                        return {'error': 'Invalid province ID'}, 400
                    
                    attractions = Attraction.objects(province=province_id)
                except Exception as e:
                    logger.error(f"Invalid province ID {province_id}: {e}")
                    return {'error': 'Invalid province ID', 'message': str(e)}, 400
            elif province_name:
                try:
                    # 根据省份名称筛选景点
                    import urllib.parse
                    province_name = urllib.parse.unquote(province_name)
                    province = Province.objects(name=province_name).first()
                    if not province:
                        return {'error': 'Province not found'}, 404
                    
                    attractions = Attraction.objects(province=province)
                except Exception as e:
                    logger.error(f"Error fetching attractions for province {province_name}: {e}")
                    return {'error': 'Invalid province name', 'message': str(e)}, 400
            else:
                attractions = Attraction.objects.all()
                
            return [attraction.to_dict() for attraction in attractions], 200
        except Exception as e:
            logger.error(f"Error fetching attractions: {e}")
            return {'error': 'Failed to fetch attractions', 'message': str(e)}, 500

class AttractionResource(Resource):
    def get(self, attraction_id):
        """获取特定景点信息"""
        try:
            attraction = Attraction.objects(id=attraction_id).first()
            if not attraction:
                return {'error': 'Attraction not found'}, 404
            return attraction.to_dict(), 200
        except Exception as e:
            logger.error(f"Error fetching attraction {attraction_id}: {e}")
            return {'error': 'Failed to fetch attraction', 'message': str(e)}, 500

def init_routes(api):
    """初始化路由"""
    api.add_resource(ProvinceListResource, '/api/provinces')
    api.add_resource(ProvinceResource, '/api/provinces/<string:province_id>')
    api.add_resource(ProvinceByNameResource, '/api/provinces/name/<string:province_name>')
    api.add_resource(AttractionListResource, '/api/attractions')
    api.add_resource(AttractionResource, '/api/attractions/<string:attraction_id>')
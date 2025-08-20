from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime

class Province(Document):
    """省份模型"""
    name = StringField(required=True, unique=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'provinces',
        'indexes': [
            'name'
        ]
    }
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Attraction(Document):
    """景点模型"""
    name = StringField(required=True)
    province = ReferenceField(Province, required=True)
    description = StringField()
    image_url = StringField()
    video_url = StringField()
    address = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'attractions',
        'indexes': [
            'name',
            'province'
        ]
    }
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'province': self.province.to_dict() if self.province else None,
            'description': self.description,
            'image_url': self.image_url,
            'video_url': self.video_url,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
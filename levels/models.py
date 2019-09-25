from mongoengine import Document, StringField, IntField, DateTimeField, ReferenceField
from core.models import CustomBaseDocument
from members.models import Member


class Level(Document, CustomBaseDocument):
    parent_level_id = ReferenceField("Level")
    title = StringField(unique=True)
    icon = StringField()
    level_no = IntField(unique=True)
    created_by = ReferenceField(Member)
    created_at = DateTimeField(required=True)
    updated_by = ReferenceField("Member")
    updated_at = DateTimeField()

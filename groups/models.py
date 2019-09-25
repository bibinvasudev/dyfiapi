from mongoengine import Document, StringField, ReferenceField, DateTimeField
from core.models import CustomBaseDocument


class Group(Document, CustomBaseDocument):
    parent_group_id = ReferenceField("Group")
    level_id = ReferenceField("Level", required=True)
    admin_id = ReferenceField("Member")
    title = StringField(unique=True)
    icon = StringField()
    created_by = ReferenceField("Member")
    created_at = DateTimeField(required=True)
    updated_by = ReferenceField("Member")
    updated_at = DateTimeField()



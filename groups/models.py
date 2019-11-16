from mongoengine import Document, StringField, ReferenceField, DateTimeField, ListField
from mongoengine import FileField
from core.models import CustomBaseDocument


class Group(Document, CustomBaseDocument):
    parent_group_id = ReferenceField("Group")
    level_id = ReferenceField("Level", required=True)
    admin_id = ReferenceField("Member")
    admin_ids = ListField(ReferenceField("Member"))
    member_ids = ListField(ReferenceField("Member"))
    title = StringField(unique=True)
    image = FileField(default="sample")
    created_by = ReferenceField("Member")
    created_at = DateTimeField(required=True)
    updated_by = ReferenceField("Member")
    updated_at = DateTimeField()

    def add_member(self, members=[], active=True):
        if not self.member_ids:
            self.member_ids = []
        for member in members:
            if member not in self.member_ids:
                self.member_ids.append(member.to_dbref())
                self.save()
            if not member.group_ids:
                member.group_ids = []
            if self not in member.group_ids:
                member.group_ids.append(self.to_dbref())
                # member.is_active = active
            member.default_group = None
            member.save()

    def get_hierarchy(self):
        path = {}
        if self.parent_group_id:
            path = self.parent_group_id.get_hierarchy()
        path.update({self.level_id.level_no: self.title})
        return path





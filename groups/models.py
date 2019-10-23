from mongoengine import Document, StringField, ReferenceField, DateTimeField, ListField
from core.models import CustomBaseDocument


class Group(Document, CustomBaseDocument):
    parent_group_id = ReferenceField("Group")
    level_id = ReferenceField("Level", required=True)
    admin_id = ReferenceField("Member")
    admin_ids = ListField(ReferenceField("Member"))
    member_ids = ListField(ReferenceField("Member"))
    title = StringField(unique=True)
    icon = StringField()
    created_by = ReferenceField("Member")
    created_at = DateTimeField(required=True)
    updated_by = ReferenceField("Member")
    updated_at = DateTimeField()

    def add_member(self, member):
        if not self.member_ids:
            self.member_ids = []
        if member.id not in self.member_ids:
            self.member_ids.append(member.id)
        if not member.group_ids:
            member.group_ids = []
        if self.id not in member.group_ids:
            member.group_ids.append(self.id)
        self.save()
        member.save()

    def get_hierarchy(self, path={}):
        if self.parent_group_id:
            self.parent_group_id.get_hierarchy(path)
        path.update({self.level_id.level_no: self.title})
        return path





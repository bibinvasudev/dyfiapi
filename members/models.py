
from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, EmbeddedDocumentField, ReferenceField
from core.models import CustomBaseDocument


class Name(EmbeddedDocument):
    first = StringField(required=True, min_length=1)
    middle = StringField(default="", required=False)
    last = StringField(required=True, min_length=1)


class Member(Document, CustomBaseDocument):
    image = StringField(required=True, default="")
    name = EmbeddedDocumentField(Name, required=True)
    dob = DateTimeField()
    mobile_no = StringField(required=True)
    group_id = ReferenceField("Group")
    level_id = ReferenceField("Level")
    created_by = ReferenceField("Member")
    created_at = DateTimeField(required=True)
    updated_by = ReferenceField("Member")
    updated_at = DateTimeField()

    class Meta:
        unique_together = ('dob', 'mobile_no')

    def get_full_name(self):
        return "{} {}".format(self.name.first, self.name.last)

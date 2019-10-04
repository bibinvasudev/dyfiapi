
from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, EmbeddedDocumentField, ReferenceField
from mongoengine import ListField
from mongoengine import IntField
from core.models import CustomBaseDocument
from core.helpers import Helper


class Name(EmbeddedDocument):
    first = StringField(required=True, min_length=3)
    middle = StringField(default="", required=False)
    last = StringField(default="")


class Member(Document, CustomBaseDocument):
    username = StringField()
    password = StringField()
    role = StringField()
    image = StringField(default="")
    age = IntField()
    gender = StringField(choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))
    name = EmbeddedDocumentField(Name, required=True)
    dob = DateTimeField()
    mobile_no = StringField(required=True, unique_with="name.first")
    group_ids = ListField(ReferenceField("Group"))
    group_id = ReferenceField("Group")
    level_id = ReferenceField("Level")
    created_by = ReferenceField("Member")
    created_at = DateTimeField()
    updated_by = ReferenceField("Member")
    updated_at = DateTimeField()

    def get_full_name(self):
        return {"first": self.name.first, "middle": self.name.middle, "last": self.name.last}

    @classmethod
    def get_registered_member(cls, payload):
        mobile_no = payload.get("mobile_no", None)
        dob = payload.get("dob", None)
        if mobile_no and dob:
            members = Member.objects.filter(dob=dob, mobile_no=mobile_no)
            if len(members) > 0:
                return members[0]
            return False
        else:
            username = payload.get("username", None)
            password = payload.get("password", None)
            members = Member.objects.filter(username=username, password=password)
            if len(members) > 0:
                return members[0]
        return False

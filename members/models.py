import datetime
from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, EmbeddedDocumentField, ReferenceField
from mongoengine import ListField
from mongoengine import IntField
from mongoengine import BooleanField
from core.models import CustomBaseDocument


class Name(EmbeddedDocument):
    first = StringField(required=True, min_length=3)
    middle = StringField(default="", required=False)
    last = StringField(required=True)


class Member(Document, CustomBaseDocument):
    username = StringField()
    password = StringField()
    role = StringField()
    blood_group = StringField()
    qualification = StringField()
    job = StringField()
    email = StringField()
    image = StringField(default="")
    age = IntField()
    gender = StringField(choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))
    name = EmbeddedDocumentField(Name, required=True)
    dob = DateTimeField()
    mobile_no = StringField(required=True, unique_with="dob")
    address = StringField()
    group_ids = ListField(ReferenceField("Group"))
    group_id = ReferenceField("Group")
    level_id = ReferenceField("Level")
    is_member_already = BooleanField(default=False)
    is_active = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    created_by = ReferenceField("Member")
    created_at = DateTimeField()
    updated_by = ReferenceField("Member")
    updated_at = DateTimeField()

    def get_full_name(self):
        return {"first": self.name.first, "middle": self.name.middle, "last": self.name.last}

    @classmethod
    def get_registered_member(cls, payload):
        mobile_no = payload.get("mobile_no", None)
        dob_str = payload.get("dob", None)
        if mobile_no and dob_str:
            dob = datetime.datetime.strptime(dob_str, "%d/%m/%Y")
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

    @property
    def is_superuser(self):
        if self.role == "superuser":
            return True
        else:
            return False

    @property
    def higher_group(self):
        groups = sorted(self.group_ids, key=lambda g: g.level_id.level_no)
        if len(groups) > 0:
            return groups[-1]
        else:
            return False

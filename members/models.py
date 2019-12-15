import datetime
from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, EmbeddedDocumentField, ReferenceField
from mongoengine import ListField
from mongoengine import IntField
from mongoengine import BooleanField
from core.models import CustomBaseDocument
from mongoengine import FileField


class Name(EmbeddedDocument):
    first = StringField(required=True, min_length=3)
    middle = StringField(default="", required=False)
    last = StringField(required=True)


class Address(EmbeddedDocument):
    house = StringField(null=True)
    street = StringField(null=True, required=False)
    city = StringField(null=True)
    district = StringField(null=True)
    state = StringField(null=True)
    pin_code = StringField(null=True)

    def __str__(self):
        return "{}, {}, {}, {}, {} {}".format(self.house, self.street, self.city, self.district, self.state, self.pin_code)


class Member(Document, CustomBaseDocument):
    username = StringField()
    password = StringField()
    role = StringField()
    blood_group = StringField()
    qualification = StringField()
    job = StringField()
    email = StringField()
    image = FileField(default="sample")
    age = IntField()
    gender = StringField(choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))
    name = EmbeddedDocumentField(Name, required=True)
    dob = DateTimeField()
    mobile_no = StringField(required=True, unique_with="dob")
    address = EmbeddedDocumentField(Address)
    group_ids = ListField(ReferenceField("Group"))
    group_id = ReferenceField("Group")
    default_group = ReferenceField("Group")
    level_id = ReferenceField("Level")
    is_member_already = BooleanField(default=False)
    is_active = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    created_by = ReferenceField("Member")
    created_at = DateTimeField()
    updated_by = ReferenceField("Member")
    updated_at = DateTimeField()

    def get_full_name(self):
        if self.name.middle:
            return '{0} {1} {2}'.format(self.name.first, self.name.middle, self.name.last)
        return '{0} {1}'.format(self.name.first, self.name.last)

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

    def get_member_details(self):
        details = {
            "id": str(self.id),
            "name": self.get_full_name(),
            "mobile_no": self.mobile_no,
            "address": self.address,
            "job": self.job,
            "age": self.age,
            "gender": self.gender,
            "email": self.email,
            "qualification": self.qualification,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "is_member_already": self.is_member_already,
            "blood_group": self.blood_group,
            "dob": datetime.datetime.strftime(self.dob, "%d/%m/%Y"),
            "level_id": str(self.level_id.id) if self.level_id else "",
            "level_no": self.level_id.level_no if self.level_id else "",
            "level_title": self.level_id.title if self.level_id else "",
            "group_ids": [str(group_id.id) for group_id in self.group_ids],
            "image": self.image.read() if self.image else ""
        }
        return details

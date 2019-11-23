import datetime
from rest_framework_mongoengine import serializers
from members.models import Member
from members.models import Name
from members.models import Address


class NameSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Name
        fields = ('first', 'middle', 'last')
        extra_kwargs = {'middle': {'allow_blank': True}}


class AddressSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class MemberSerializer(serializers.EmbeddedDocumentSerializer):

    name = NameSerializer()
    address = AddressSerializer()
    dob = serializers.serializers.SerializerMethodField()
    group_ids = serializers.serializers.SerializerMethodField()
    image = serializers.serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ('id', 'mobile_no', 'dob', 'name', 'gender', 'blood_group', 'qualification', 'job', 'email', 'age',
                  'address', 'group_ids', 'level_id', 'is_admin', 'is_active', 'address', "image")

    def get_group_ids(self, obj):
        return [str(group.id) for group in obj.group_ids]

    def get_image(self, obj):
        return obj.image.read() if obj.image else ""

    def get_dob(self, obj):
        return datetime.datetime.strftime(obj.dob, "%d/%m/%Y")


class MemberSimpleSerializer(serializers.EmbeddedDocumentSerializer):

    name = NameSerializer()
    address = AddressSerializer()
    group_ids = serializers.serializers.SerializerMethodField()
    image = serializers.serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ('id', 'mobile_no', 'name', 'address', 'group_ids', 'is_admin', 'is_active', "image")

    def get_group_ids(self, obj):
        return [str(group.id) for group in obj.group_ids]

    def get_image(self, obj):
        return obj.image.read() if obj.image else ""

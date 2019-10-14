from rest_framework_mongoengine import serializers
from members.models import Member
from members.models import Name


class NameSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Name
        fields = ('first', 'middle', 'last')
        extra_kwargs = {'middle': {'allow_blank': True}}


class MemberSerializer(serializers.EmbeddedDocumentSerializer):

    name = NameSerializer()

    class Meta:
        model = Member
        fields = ('mobile_no', 'dob', 'name', 'gender', 'blood_group', 'qualification', 'job', 'email', 'age',
                  'address', 'group_ids', 'level_id', 'is_member_already')

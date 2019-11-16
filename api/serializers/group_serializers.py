from rest_framework_mongoengine import serializers
from groups.models import Group


class GroupSerializer(serializers.EmbeddedDocumentSerializer):
    level_no = serializers.serializers.SerializerMethodField()
    level_title = serializers.serializers.SerializerMethodField()
    admin_ids = serializers.serializers.SerializerMethodField()
    member_ids = serializers.serializers.SerializerMethodField()
    parent_group_name = serializers.serializers.SerializerMethodField()
    image = serializers.serializers.SerializerMethodField()
    hierarchy = serializers.serializers.SerializerMethodField()
    members_count = serializers.serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'title', 'level_id', 'level_no', 'level_title', 'admin_ids', 'member_ids', 'parent_group_name',
                  'hierarchy', 'members_count', 'image')

    def get_level_no(self, obj):
        return obj.level_id.level_no

    def get_level_title(self, obj):
        return obj.level_id.title

    def get_admin_ids(self, obj):
        return [str(admin.id) for admin in obj.admin_ids]

    def get_member_ids(self, obj):
        return [str(member.id) for member in obj.member_ids]

    def get_parent_group_name(self, obj):
        return obj.parent_group_id.tittle if obj.parent_group_id else ""

    def get_image(self, obj):
        return obj.image.read() if obj.image else ""

    def get_hierarchy(self, obj):
        return obj.get_hierarchy()

    def get_members_count(self, obj):
        members = obj.member_ids
        active_count = len([m for m in members if m.is_active])
        inactive_count = len(members) - active_count
        return {"total": len(members), "active": active_count, "inactive": inactive_count}

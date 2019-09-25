from bson import ObjectId


class CustomBaseDocument:
    meta = {'allow_inheritance': True}

    @classmethod
    def safe_get(cls, object_id):
        if not ObjectId.is_valid(object_id):
            return None
        return cls.objects.with_id(object_id)



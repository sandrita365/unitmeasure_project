from rest_framework import serializers

from .models import UnitMeasure


class InUnitMeasureSerializer(serializers.ModelSerializer):
    """
    This class is a UnitMeasure serializer; it defines the features for each input field.
    """
    name: str = serializers.CharField(max_length=100, required=False,
                                      allow_blank=False)
    abbreviation: str = serializers.CharField(max_length=50, required=False,
                                              allow_blank=False)
    description: str = serializers.CharField(max_length=250, required=False,
                                             allow_blank=True)

    class Meta:
        model = UnitMeasure
        fields = ("name", "abbreviation", "description")


class OutUnitMeasureSerializer(serializers.ModelSerializer):
    """
    This class is a UnitMeasure serializer; it defines the features for each output field.
    """
    name: str = serializers.CharField(max_length=100, required=True)
    abbreviation: str = serializers.CharField(max_length=50, required=False,
                                              allow_blank=False)
    description: str = serializers.CharField(max_length=250, required=False,
                                             allow_blank=True)

    class Meta:
        model = UnitMeasure
        fields = ("name", "abbreviation", "description")


class OutInitMeasureWithIdSerializer(OutUnitMeasureSerializer):
    """
    This class is a UnitMeasure serializer; it defines the features for each output field,
     furthermore, the _id field is converted to a string.
    """
    _id = serializers.SerializerMethodField()

    class Meta:
        model = UnitMeasure
        fields = ("_id", "name", "abbreviation", "description")

    def get__id(self, obj):
        return str(obj._id)

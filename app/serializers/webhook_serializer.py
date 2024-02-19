from rest_framework import serializers


class DealSerializer(serializers.Serializer):
    person_name = serializers.CharField()
    org_id = serializers.IntegerField()
    value = serializers.DecimalField(decimal_places=2, max_digits=10)
    id = serializers.IntegerField()
    stage_id = serializers.IntegerField()
    person_id = serializers.IntegerField()
    org_id = serializers.IntegerField()


class DealSerializerUpdate(serializers.Serializer):
    stage_order_nr = serializers.IntegerField()
    id = serializers.IntegerField()
    person_name = serializers.CharField()


class CoreToPipedriveIntegrationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    investment_id = serializers.IntegerField(required=False, allow_null=True)

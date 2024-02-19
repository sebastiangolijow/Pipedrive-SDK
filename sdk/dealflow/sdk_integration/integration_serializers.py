from rest_framework import serializers


class StartuptoOrganizationSerializer(serializers.Serializer):
    """Serializer to validate data coming from investment to create deal in pipedrive"""

    startup_name = serializers.CharField()
    location = serializers.IntegerField()
    website = serializers.CharField(required=False, allow_null=True)
    sectors_of_interest = serializers.ListField(required=False, allow_null=True)
    business_models = serializers.ListField()
    go_to_markets = serializers.ListField(required=False, allow_null=True)
    tagline = serializers.CharField()
    growth_stage = serializers.IntegerField()
    address = serializers.CharField()

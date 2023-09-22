from rest_framework import serializers

class AddressInputSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=200)
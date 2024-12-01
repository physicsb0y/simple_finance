from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.db import transaction

from .models import Address


User = get_user_model()

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'province', 'city', 'zip_code', 'street']

class UserCreateSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'phone_numbers',
            'date_of_birth',
            'citizenship_number',
            'address'
        ]

    def create(self, validated_data):
        with transaction.atomic():
            address_data = validated_data.pop('address')
            address = Address.objects.create(**address_data)
            validated_data['address'] = address
            
            user = get_user_model().objects.create_user(
                **validated_data
            )
            user.save()
            return user
        
    def update(self, instance, validated_data):
        with transaction.atomic():
            address_data = validated_data.pop('address', None)
        
            if address_data:
                if instance.address:
                    for key, value in address_data.items():
                        setattr(instance.address, key, value)
                    instance.address.save()
                else:
                    instance.address = Address.objects.create(**address_data)
            

            for attr, value in validated_data.items():
                if attr == 'password':
                    instance.set_password(value)
                else:
                    setattr(instance, attr, value)
            
            instance.save()
            return instance



class UserDisplaySerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_numbers',
            'date_of_birth',
            'citizenship_number',
            'address'
        ]

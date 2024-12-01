from rest_framework import serializers

from django.db import transaction

from .models import Expense, ExpenseCategory, Income



class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'source_name', 'amount', 'date_received', 'status', 'notes']
        read_only_fields = ['id']


class ExpenseCategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'user', 'name', 'description']
        read_only_fields = ['id', 'user']



class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    category = ExpenseCategorySerializer()

    class Meta:
        model = Expense
        fields = ['id', 'user', 'category', 'amount', 'due_date', 'status', 'notes']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        category = validated_data.pop('category')
        with transaction.atomic():
            category_instance, created = ExpenseCategory.objects.get_or_create(**category)
            validated_data['category'] = category_instance
            return super().create(validated_data)
        
    def update(self, instance, validated_data):
        category = validated_data.pop('category')
        with transaction.atomic():
            category_instance, created = ExpenseCategory.objects.get_or_create(**category)
            validated_data['category'] = category_instance
            return super().update(instance, validated_data)

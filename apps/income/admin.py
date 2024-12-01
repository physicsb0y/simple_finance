from django.contrib import admin

from .models import Income, ExpenseCategory, Expense

# Register your models here.

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'source_name', 'amount', 'date_received', 'status']
    list_filter = ['user', 'status', 'amount']
    search_fields = ['user', 'source_name', 'amount', 'status']
    readonly_fields = ['id']



@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name']
    list_filter = ['user', 'name']
    search_fields = ['user', 'name']




@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'category', 'amount', 'due_date', 'status']
    list_filter = ['user', 'category', 'amount', 'status']
    search_fields = ['user', 'category']

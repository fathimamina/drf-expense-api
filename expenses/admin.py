from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'amount', 'user', 'created_at')  # show user in list
    list_filter = ('user',)  # optional: filter by user in sidebar
    search_fields = ('title', 'user__username')  # optional: search by title or user

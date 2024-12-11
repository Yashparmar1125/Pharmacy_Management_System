from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import CustomUser, Doctor, Medicine, Manufacturer, Category, Inventory, Customer, Bill, Prescription, \
    MedDetails, Orders, Incomes, Expenses

admin.site.site_header = 'Welcome Admin!!'
admin.site.site_title = 'Welcome Admin!!'
admin.site.index_title = 'Welcome to the PharmEasy Admin Portal'

class UserModelAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'profile_pic', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, UserModelAdmin)
admin.site.register(Doctor)
admin.site.register(Medicine)
admin.site.register(Manufacturer)
admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(Customer)
admin.site.register(Bill)
admin.site.register(Prescription)
admin.site.register(MedDetails)
admin.site.register(Orders)
admin.site.register(Incomes)
admin.site.register(Expenses)

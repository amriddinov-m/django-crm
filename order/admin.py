from django.contrib import admin

from order.models import SettingStatus, Team, WashOrder, WashOrderItem, Setting


@admin.register(SettingStatus)
class SettingStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(WashOrder)
class WashOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(WashOrderItem)
class WashOrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass



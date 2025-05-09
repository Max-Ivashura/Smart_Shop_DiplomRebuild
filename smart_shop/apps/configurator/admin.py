from django.contrib import admin

from apps.configurator.models import PCBuild, BuildComponent


@admin.register(PCBuild)  
class PCBuildAdmin(admin.ModelAdmin):  
    list_display = ('id', 'user', 'total_price', 'is_public', 'is_verified')  
    list_filter = ('is_public', 'is_verified')  

@admin.register(BuildComponent)  
class BuildComponentAdmin(admin.ModelAdmin):  
    list_display = ('build', 'product', 'quantity')  
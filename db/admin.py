from django.contrib import admin
from db.models import *

class food_deliveryAdmin(admin.ModelAdmin):
	list_display = ("name","start_time","end_time")

class kitchen_dataAdmin(admin.ModelAdmin):
	list_display = ("name","spec_location","pop_food","description","foodtype","foodlevel")
	filter_horizontal = ["fooddelivery"]

class user_dataAdmin(admin.ModelAdmin):
	list_display = ("user_object","mobile","status")

class ordersAdmin(admin.ModelAdmin):
	list_display = ("user","start_date","end_date","course","address","landmark","mobile","is_active")

class picturesAdmin(admin.ModelAdmin):
	list_display = ("title","caption","kitchen","pic_category","photo","display_as_main")

class crumbsAdmin(admin.ModelAdmin):
	list_display = ("order","options","date","address","landmark","mobile")

class messagesAdmin(admin.ModelAdmin):
	list_display = ("name","email","message")

admin.site.register(location)
admin.site.register(food_type)
admin.site.register(food_level)
admin.site.register(food_course)
admin.site.register(food_delivery,food_deliveryAdmin)
admin.site.register(kitchen_data,kitchen_dataAdmin)
admin.site.register(user_data,user_dataAdmin)
admin.site.register(orders,ordersAdmin)
admin.site.register(price_list)
admin.site.register(crumb_data)
admin.site.register(messages,messagesAdmin)
admin.site.register(crumbs,crumbsAdmin)


admin.site.register(pictures,picturesAdmin)
#admin.site.register(delivery_time)
admin.site.register(pic_category)
admin.site.register(reset_key)
#admin.site.register(food_course)
#admin.site.register(city)
#admin.site.register(food_course,food_courseAdmin)
#admin.site.register(kitchen_data,kitchen_dataAdmin)

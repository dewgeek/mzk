from django.contrib import admin
from tester.models import *

class food_deliveryAdmin(admin.ModelAdmin):
	list_display = ("name","start_time","end_time")

class kitchen_dataAdmin(admin.ModelAdmin):
	list_display = ("name","spec_location","pop_food","description","foodtype","foodlevel")
	filter_horizontal = ["fooddelivery"]

class user_dataAdmin(admin.ModelAdmin):
	list_display = ("user_object","mobile","status")


admin.site.register(location)
admin.site.register(food_type)
admin.site.register(food_level)
admin.site.register(food_course)
admin.site.register(food_delivery,food_deliveryAdmin)
admin.site.register(kitchen_data,kitchen_dataAdmin)
admin.site.register(pic_category)
admin.site.register(pictures)
#admin.site.register(pictures,pictures_dataAdmin)
#admin.site.register(delivery_time)
#admin.site.register(pic_category)
#admin.site.register(food_course)
#admin.site.register(city)
#admin.site.register(food_course,food_courseAdmin)
#admin.site.register(kitchen_data,kitchen_dataAdmin)

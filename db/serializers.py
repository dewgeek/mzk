from rest_framework import serializers
from models import *
 
 
class KitchenSerializer(serializers.ModelSerializer):
	api_url = serializers.SerializerMethodField('get_api_url')
	 
	class Meta:
		model = kitchen_data
		
	 
	def get_api_url(self, obj):
		return "#/kitchen/%s" % obj.id
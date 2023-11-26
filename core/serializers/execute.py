from rest_framework import serializers
from core.models.execute import FileScript

class FileScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileScript
        fields = '__all__'

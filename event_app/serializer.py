from rest_framework import serializers # type: ignore
from .models import Events
from .models import Sessions
from .models import Speakers

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = '__all__'


class EventSerializerAdd(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields='__all__'

class EventSerializerGet(serializers.ModelSerializer):
    sessions= SessionSerializer(many=True)
    class Meta:
        model = Events
        fields = ['id','title','description','date','location','created_at','updated_at','sessions']
     

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speakers
        fields = '__all__'
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Post
        fields = ('id',
        'title',
        'published',
        'created_date',
        'text',
        'published_date')
    
    # def to_representation(self, instance):
    #     if instance.published_date:
    #         formatted_datetime_field = instance.published_date.timestamp()
    #     else:
    #         formatted_datetime_field = None

    #     return {'id': instance.id, 'title': instance.title, 'published': instance.published, 'created_date':instance.created_date,
    #      'text':instance.text, 'published_date': formatted_datetime_field}
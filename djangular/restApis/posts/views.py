from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import datetime
 
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()

        title = request.query_params.get('title', None)
        if title is not None:
            posts = posts.filter(title__icontains=title)
        
        posts_serializer = PostSerializer(posts, many=True)
        #for date in posts_serializer.data:
        #    if date.get('published_date'):
        #        date['published_date'] = datetime.datetime(date['published_date']).timestamp()
        # if posts_serializer.data[0].get('published_date'):
        #     posts_serializer.data['published_date'] = posts_serializer.validated_data.get('published_date').timestamp()
        return JsonResponse(posts_serializer.data, safe = False)

    elif request.method == 'POST':
        post_data = JSONParser().parse(request)
        posts_serializer = PostSerializer(data=post_data)
        if posts_serializer.is_valid():
            posts_serializer.save()
            return JsonResponse(posts_serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Post.objects.all().delete()
        return JsonResponse({'message': '{} Posts were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    try:
        posts = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'message': 'The post does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET':
        posts_serializer = PostSerializer(posts)
        return JsonResponse(posts_serializer.data)
    
    elif request.method == 'PUT':
        post_data = JSONParser().parse(request)
        posts_serializer = PostSerializer(posts, data=post_data)
        if posts_serializer.is_valid():
            if posts_serializer.validated_data.get("published") == True:
                posts.publish(True)
            else:
                posts.publish(False)
                
            posts_serializer.save()
            return JsonResponse(posts_serializer.data)
        return JsonResponse(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        posts.delete()
        return JsonResponse({'message': 'Post was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def post_list_published(request):
    posts = Post.objects.filter(published = True)

    if request.method == 'GET':
        posts_serializer = PostSerializer(posts, many=True)
        return JsonResponse(posts_serializer.data, safe=False)
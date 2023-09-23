from django.db import IntegrityError
from django.http import JsonResponse
from .models import *

def handle_post_like_creation(post, user):
    try:
        PostLike.create_PostLike(post=post, user=user, currentLike=True)
        return JsonResponse({"success": "post liked"})
    except IntegrityError:
        return JsonResponse({"error": "could not create post like record"}, status=400)
    

def update_post_like_count(post):
    postLikeCount = PostLike.objects.filter(post=post, currentLike=True).count()
    post.likeCount = postLikeCount
    post.save()

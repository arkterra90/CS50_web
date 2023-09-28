from django.db import IntegrityError
from django.http import JsonResponse
from .models import *

# creates a new post like in the PostLike model.
def handle_post_like_creation(post, user):
    try:
        PostLike.create_PostLike(post=post, user=user, currentLike=True)
        return JsonResponse({"success": "post liked"})
    except IntegrityError:
        return JsonResponse({"error": "could not create post like record"}, status=400)
    
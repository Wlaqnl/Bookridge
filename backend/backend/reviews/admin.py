from django.contrib import admin
from .models import Review, ReviewComment, ReviewLike, Phrase
# Register your models here.

admin.site.register(Review)
admin.site.register(ReviewComment)
admin.site.register(ReviewLike)
admin.site.register(Phrase)

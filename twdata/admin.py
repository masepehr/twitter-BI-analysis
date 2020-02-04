from django.contrib import admin
from .models import Persons,Tweets


# class TweetInlines(admin.TabularInline):
#     model = Tweets
#     class Meta:
#         fields=['text']
class PersonInline(admin.TabularInline):
    model = Persons
class TweetAdmin(admin.ModelAdmin):

    list_display = ('author','text')
    list_filter = ('author',)


admin.site.register(Persons)

admin.site.register(Tweets,TweetAdmin)
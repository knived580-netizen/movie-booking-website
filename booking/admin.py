from django.contrib import admin
from .models import Movie, Theatre, Show, Booking

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'price', 'gst_percentage')
    list_editable = ('price', 'gst_percentage')

admin.site.register(Movie, MovieAdmin)
admin.site.register(Theatre)
admin.site.register(Show)
admin.site.register(Booking)
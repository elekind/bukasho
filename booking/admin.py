from django.contrib import admin
from .models import Movie, ID, Hall, Seat, Show, Booking

admin.site.register(Movie)
admin.site.register(ID)
admin.site.register(Hall)
admin.site.register(Seat)
admin.site.register(Show)
admin.site.register(Booking)

admin.site.site_header = "User: Stranger \n Pwd: Bukasho123!"
admin.site.site_title = "Manage Bukasho"
admin.site.index_title = "Welcome to Bukasho Admin"

# Register your models here.

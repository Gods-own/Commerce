from django.contrib import admin

from .models import Auctions, Category, Bid, Comments, Watch, User

# Register your models here.
admin.site.register(User)
admin.site.register(Auctions)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(Watch)

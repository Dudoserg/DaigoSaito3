from django.contrib import admin
from .models import Post
from .models import Material, Product, Technology_map, Technology_map_position


admin.site.register(Post)
admin.site.register(Material)
admin.site.register(Product)
admin.site.register(Technology_map)
admin.site.register(Technology_map_position)

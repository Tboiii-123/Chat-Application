from django.contrib import admin

# Register your models here.


from .models import Profile,ChatMessage,Friend


admin.site.register([Profile,ChatMessage,Friend])

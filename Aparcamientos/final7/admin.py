from django.contrib import admin

# Register your models here.
from final7.models import Aparcamiento
from final7.models import Comentario
from final7.models import Pag_Usuario


admin.site.register(Aparcamiento)
admin.site.register(Comentario)
admin.site.register(Pag_Usuario)

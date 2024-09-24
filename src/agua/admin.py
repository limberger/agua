from django.contrib import admin
from agua.models import Condominio, Condomino, Hidrometro, Medicao, TipoDespesa, Despesa, Competencia

# Register your models here.
admin.site.register(Condominio)
admin.site.register(Condomino)
admin.site.register(Hidrometro)
admin.site.register(TipoDespesa)
admin.site.register(Despesa)
admin.site.register(Competencia)

@admin.register(Medicao)
class MedicaoAdmin(admin.ModelAdmin):
     ordering = ['-cmpt','hidrometro','medicao']
     list_display = ['cmpt','hidrometro','medicao' , 'consumo']

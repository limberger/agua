from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Familia(models.Model):
    PARENTESCO_CHOICES = (
    ('Filha', 'Filho/Filha'),
    ('Enteada', 'Enteado/Enteada'),
    ('Mãe', 'Pai/Mãe'),
    ('Esposa', 'Esposa/Esposo'),
    ('Responsável', 'Responsável'),
    ('Sobrinha', 'Sobrinho/Sobrinha'),
    ('Tia', 'Tio/Tia'),
    ('Prima', 'Primo/Prima'),
    ('Neta', 'Neto/Neta'),
    ('Bisneta', 'Bisneto/Biseta'),
    ('Ava', 'Avo/Avó'),
    ('Nora', 'Genro/Nora'),
    ('Cunhada', 'Cunhado/Cunhada'),
    ('Bisava', 'Bisavo/Bisavó'),
    ('Parente', 'Outro parente'),
    ('Amiga', 'Amigo/Amiga'),
    ('Outra', 'Outro/Outra'),
    )
    UF_CHOICES = (
    ('AC','Acre'),
    ('AL','Alagoas'),
    ('AM','Amazonas'),
    ('AP','Amapá'),
    ('BA','Bahia'),
    ('CE','Ceará'),
    ('DF','Distrito Federal'),
    ('ES','Espirito Santo'),
    ('GO','Goiás'),
    ('MA','Maranhão'),
    ('MG','Minas Gerais'),
    ('MS','Mato Grosso do Sul'),
    ('MT','Mato Grosso'),
    ('PA','Pará'),
    ('PB','Paraiba'),
    ('PE','Pernambuco'),
    ('PI','Piauí'),
    ('PR','Paraná'),
    ('RJ','Rio de Janeiro'),
    ('RN','Rio Grande do Norte'),
    ('RO','Rondönia'),
    ('RR','Roraima'),
    ('RS','Rio Grande do Sul'),
    ('SC','Santa Catarina'),
    ('SE','Sergipe'),
    ('SP','São Paulo'),
    ('TO','Tocantins'),
    ('','-'),
    )
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL,
      null=True, blank=True, on_delete=models.SET_NULL)
    nome_conhecido = models.CharField(max_length=51)
    nome_completo = models.CharField(max_length=150)
    vira_para_o_encontro = models.BooleanField()
    telefone = models.CharField(max_length=30,blank=True)
    parentesco = models.CharField(max_length=20,choices=PARENTESCO_CHOICES,default='Outro')
    email = models.EmailField(max_length=254,blank=True)
    data_nascimento = models.DateField(auto_now=False,
    auto_now_add=False)
    endereco_correspondencia = models.CharField(max_length=200,blank=True)
    cep_correspondencia = models.CharField(max_length=9,blank=True)
    cidade_correspondencia = models.CharField(max_length=100,blank=True)
    estado_correspondencia = models.CharField(max_length=2,choices=UF_CHOICES,default='',blank=True)
    comentario = models.CharField(max_length=512,blank=True)


    def is_responsavel(self):
        return self.parentesco == 'Resp'

    def __str__(self):
        return self.nome_conhecido + " [" + self.nome_completo + "]"

    def get_absolute_url(self):
        return reverse('familia_edit',kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.id:
            super(Familia, self).save(*args,**kwargs)

    # def save_model(self, request, instance, form, change):
    #     user = request.user
    #     instance = form.save(commit=False)
    #     if not change or not instance.usuario_responsavel:
    #         instance.usuario_responsavel = user
    #     instance.save()
    #     form.save_m2m()
    #     return instance

# Generated by Django 2.1.2 on 2018-10-20 14:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_conhecido', models.CharField(max_length=50)),
                ('nome_completo', models.CharField(max_length=150)),
                ('vira_para_o_encontro', models.BooleanField()),
                ('telefone', models.CharField(blank=True, max_length=30)),
                ('parentesco', models.CharField(choices=[('Filha', 'Filho/Filha'), ('Enteada', 'Enteado/Enteada'), ('Mãe', 'Pai/Mãe'), ('Esposa', 'Esposa/Esposo'), ('Responsável', 'Responsável'), ('Sobrinha', 'Sobrinho/Sobrinha'), ('Tia', 'Tio/Tia'), ('Prima', 'Primo/Prima'), ('Neta', 'Neto/Neta'), ('Bisneta', 'Bisneto/Biseta'), ('Ava', 'Avo/Avó'), ('Nora', 'Genro/Nora'), ('Cunhada', 'Cunhado/Cunhada'), ('Bisava', 'Bisavo/Bisavó'), ('Parente', 'Outro parente'), ('Amiga', 'Amigo/Amiga'), ('Outra', 'Outro/Outra')], default='Outro', max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('data_nascimento', models.DateField()),
                ('endereco_correspondencia', models.CharField(blank=True, max_length=200)),
                ('cep_correspondencia', models.CharField(blank=True, max_length=9)),
                ('cidade_correspondencia', models.CharField(blank=True, max_length=100)),
                ('estado_correspondencia', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AM', 'Amazonas'), ('AP', 'Amapá'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espirito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MG', 'Minas Gerais'), ('MS', 'Mato Grosso do Sul'), ('MT', 'Mato Grosso'), ('PA', 'Pará'), ('PB', 'Paraiba'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('PR', 'Paraná'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RO', 'Rondönia'), ('RR', 'Roraima'), ('RS', 'Rio Grande do Sul'), ('SC', 'Santa Catarina'), ('SE', 'Sergipe'), ('SP', 'São Paulo'), ('TO', 'Tocantins'), ('', '-')], default='', max_length=2)),
                ('comentario', models.CharField(blank=True, max_length=512)),
                ('usuario_responsavel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

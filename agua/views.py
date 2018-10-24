
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib import messages

from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import ModelForm, DateInput, Textarea , TextInput

from agua.models import Agua
from django.utils.translation import ugettext_lazy as _

from social_django.models import UserSocialAuth

import logging

class DateInput(DateInput):
    input_type = 'date'

class TelInput(TextInput):
    input_type = 'tel'

class EmailInput(TextInput):
    input_type = 'email'


class AguaForm(ModelForm):
    class Meta:
        model = Agua
        fields = ['usuario_responsavel' ,
                  'nome_conhecido' ,
                  'nome_completo' ,
                  'vira_para_o_encontro' ,
                  'telefone' ,
                  'parentesco' ,
                  'email' ,
                  'data_nascimento' ,
                  'endereco_correspondencia' ,
                  'cep_correspondencia' ,
                  'cidade_correspondencia' ,
                  'estado_correspondencia',
                  'comentario']
        help_texts = {
            'nome_conhecido': _('Informe o nome ou apelido pelo qual é conhecido'),
            'vira_para_o_encontro': _('Informe se virá para o encontro'),

        }
        labels = {
            'nome_conhecido': _('Nome/Apelido'),
            'nome_completo': _('Nome Completo'),
            'endereco_correspondencia': _('Endereço'),
            'cidade_correspondencia': _('Cidade'),
            'estado_correspondencia': _('Estado'),
            'cep_correspondencia': _('CEP'),

        }
        error_messages = {
            'nome_conhecido': {
                'max_length': _("O nome está muito comprido."),
            },
        }
        widgets = {
           'nome_conhecido': TextInput(attrs={'size':'20'}),
           'nome_commpleto': TextInput(attrs={'size':'80'}),
           'email': EmailInput(attrs={'size':'80'}),
           'data_nascimento': DateInput(),
           'telefone': TelInput(attrs={'placeholder':'61-99635-6601'}),
           'cep_correspondencia': TextInput(attrs={'placeholder':'80000-000'}),
           'comentario': Textarea(attrs={'rows':4,'cols':50})
        }
        exclude = ['usuario_responsavel']
"""
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL,
      null=True, blank=True, on_delete=models.SET_NULL)
    nome_conhecido = models.CharField(max_length=55)
    nome_completo = models.CharField(max_length=200)
    vira_para_o_encontro = models.BooleanField()
    telefone = models.CharField(max_length=20,blank=True)
    parentesco = models.CharField(max_length=20,
    choices=PARENTESCO_CHOICES,
    default='Outro')
    email = models.EmailField(max_length=254,blank=True)
    data_nascimento = models.DateField(auto_now=False,auto_now_add=False)
    endereco_correspondencia = models.CharField(max_length=200,blank=True)
    cep_correspondencia = models.CharField(max_length=9,blank=True)
    cidade_correspondencia = models.CharField(max_length=100,blank=True)
    estado_correspondencia = models.CharField(max_length=2,blank=True)
    comentario = models.CharField(max_length=512,blank=True)
"""
    # def __init__(self, *args, **kwargs):
    #    self.request = kwargs.pop('request', None)
    #    return super(AguaForm, self).__init__(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     kwargs['commit']=False
    #     obj = super(AguaForm, self).save(*args, **kwargs)
    #     if self.request:
    #         obj.usuario_responsavel = self.request.user
    #     obj.save()
    #     return obj

    # def __init__(self,user,*args, **kwargs):
    #      self.request = kwargs.pop('request')
    #      return super(PatientForm,self).__init__(*args,**kwargs)
    #
    #
    # def save(self, *args, **kwargs):
    #     kwargs['commit'] = False
    #     obj = super(Agua_Form.self).save(*args,**kwargs)
    #     if self.request:
    #         obj.usuario_responsaavel = self.request.user
    #     obj.save()
@login_required
def home(request):
    return render(request, 'agua/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            #login(request, user,backend='django.contrib.auth.backends.ModelBackend)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html',{'form': form})


@login_required
def settings(request):
    user = request.user

    # try:
    #     github_login = user.social_auth.get(provider='github')
    # except UserSocialAuth.DoesNotExist:
    #     github_login = None

    # try:
    #     twitter_login = user.social_auth.get(provider='twitter')
    # except UserSocialAuth.DoesNotExist:
    #     twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'settings.html', {
        # 'github_login': github_login,
        # 'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'agua/password.html', {'form': form})


@login_required
def agua_list(request, template_name='agua/agua_list.html'):
    logger = logging.getLogger('testlogger')
    logger.info('agua_list')
    responsavel = Agua.objects.filter(usuario_responsavel=request.user.id,
                            parentesco = 'Responsável')
    if not responsavel:
        form = AguaForm(request.POST or None)
        request.session['parentesco'] = 'Responsável'
        request.session['obs']  = 'Cadastre inicialmente o responsável pela família (o usuário que se cadastrou).'
        return redirect('/agua/new')

    agua = Agua.objects.filter(usuario_responsavel=request.user.id)
    data = {}
    data['object_list'] = agua
    return render(request, template_name, data)

@login_required
def agua_view(request, pk , template_name='agua/agua_detail.html'):
    agua = get_object_or_404(Agua, pk=pk)
    return render(request, template_name, {'object':agua})

@login_required
def agua_create(request, template_name='agua/agua_form.html'):
    logger = logging.getLogger('testlogger')
    logger.info('agua_create')
    form = AguaForm(request.POST or None)
    obs=''
    if request.session['obs']:
        obs = request.session['obs']
        request.session['obs'] = None
    if request.session['parentesco']:
        logger.info('setting parentesco')
        logger.info(request.session['parentesco'])
        form = AguaForm(initial={'parentesco': request.session['parentesco'] })
        request.session['parentesco'] = None
    if form.is_valid():
        form0 = form.save(commit=False)
        form0.usuario_responsavel = request.user
        form0.save()
        return redirect('/agua/')
    return render(request, template_name, {'form':form , 'obs':obs})

@login_required
def agua_update(request, pk , template_name='agua/agua_form.html'):
    agua = get_object_or_404(Agua, pk=pk)
    form = AguaForm(request.POST or None, instance=agua)
    if form.is_valid():
        form.save()
        return redirect('/agua/')
    return render(request, template_name, {'form':form})

@login_required
def agua_delete(request, pk , template_name='agua/agua_confirm_delete.html'):
    agua = get_object_or_404(Agua, pk=pk)
    if request.method=='POST':
        agua.delete()
        return redirect('/agua/')
    return render(request, template_name, {'object':agua})

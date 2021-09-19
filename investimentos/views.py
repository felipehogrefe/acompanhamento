from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, JsonResponse
from investimentos.models import Acao, UsuarioAcao, recuperar_acao
from django.template.defaultfilters import register


class IndexView(generic.TemplateView):
    template_name = 'investimentos/index.html'


def importar_preferencias(request):
    return HttpResponse(status=200)


def exportar_preferencias(request):
    return HttpResponse(status=200)


def buscar_acao(request):
    sigla = request.GET.get('sigla')
    acoes = []
    if sigla:
        acoes = Acao.objects.filter(sigla__icontains=sigla)

    return JsonResponse({'status': 200, 'data': [acao.sigla for acao in acoes]})


def adicionar_acao(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        sigla_acao = request.POST.get('sigla-acao')
        usuario_acao = recuperar_acao(user, sigla_acao)
    return redirect(reverse('investimentos:index'))


@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)

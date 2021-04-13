from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Empresa
from core.forms.empresas_forms import EmpresasForm


def index(request, template_name='administracao/paginas/index.html'):
    return render(request, template_name)


def listar_empresas(request, template_name="administracao/paginas/empresas_edit.html"):
    if request.user.is_superuser:
        empresas = Empresa.objects.all()
        empresas_cadastradas = {'empresas': empresas}

        return render(request, template_name, empresas_cadastradas)
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('index')


def cadastrar_empresas(request, template_name='administracao/empresas/empresas_form.html'):
    if request.user.is_superuser:

        if request.method == 'POST':
            form = EmpresasForm(request.POST or None)
            if form.is_valid():
                empresa = form.save(commit=False)
                empresa.save()
                messages.success(request, "Empresa cadastrada com sucesso!")
                return redirect('listar_empresas')
            else:
                messages.error(request, "Ops, não foi possivel cadastrar a empresa")
        else:
            form = EmpresasForm()
        return render(request, template_name, {'form': form})

    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('index')
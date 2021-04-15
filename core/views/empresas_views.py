from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from core.models import Empresa
from core.forms.empresas_forms import EmpresasForm
from usuario.models import Usuario
from api.models import Produto
from django.contrib.auth.models import User


def index(request, template_name='administracao/paginas/index.html'):
    return render(request, template_name)


def listar_empresas(request, template_name="administracao/empresas/empresas.html"):
    if request.user.is_superuser:
        empresas = Empresa.objects.all()
        empresas_cadastradas = {'empresas': empresas}

        return render(request, template_name, empresas_cadastradas)
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('index')


def cadastrar_empresa(request, template_name='administracao/empresas/empresas_form.html'):
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


def editar_empresa(request, pk, template_name='administracao/empresas/empresas_form.html'):
    if request.user.is_superuser:
        empresa = get_object_or_404(Empresa, pk=pk)
        if request.method == 'POST':
            form = EmpresasForm(request.POST, instance=empresa)
            if form.is_valid():
                empresa = form.save(commit=False)
                empresa.save()
                messages.success(request, "Empresa atualizada com sucesso!")
                return redirect('listar_empresas')
            else:
                messages.error(request, "Ops, não foi possivel cadastrar a empresa")
        else:
            form = EmpresasForm(instance=empresa)
        return render(request, template_name, {'form': form})
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('index')




def detalhes_empresa(request, pk, template_name='administracao/empresas/empresas_detalhes.html'):
    empresa = get_object_or_404(Empresa, pk=pk)
    usuarios = Usuario.objects.filter(empresa=empresa.pk)

    return render(request, template_name, {'empresa': empresa, 'usuarios': usuarios})




#PEGAR EMPRESA E PRODUTOS DO USUARIO LOGADO
#usuario_id = request.user.id
#empresa = Empresa.objects.filter(empresa__usuario_id=usuario_id)
#print(empresa)
#produtos = list(Produto.objects.filter(empresa_id=1).values())
#print(produtos)
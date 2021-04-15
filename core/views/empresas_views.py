from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models import Empresa
from core.forms.empresas_forms import EmpresasForm
from usuario.models import Usuario


"""

View de cadastro, edição, ataulização, listagem, ativação e desativação de empresas
As as funções desta view são especificas para a administração do sistema, o acesso é
permitido para superusuarios autenticados.

"""

@login_required
def index(request, template_name='administracao/paginas/index.html'):
    return render(request, template_name)


@login_required
def listar_empresas(request, template_name="administracao/empresas/empresas.html"):
    if request.user.is_superuser:
        empresas = Empresa.objects.all()
        empresas_cadastradas = {'empresas': empresas}

        return render(request, template_name, empresas_cadastradas)
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('index')


@login_required
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


@login_required
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


@login_required
def detalhes_empresa(request, pk, template_name='administracao/empresas/empresas_detalhes.html'):
    empresa = get_object_or_404(Empresa, pk=pk)
    usuarios = Usuario.objects.filter(empresa=empresa.pk)

    return render(request, template_name, {'empresa': empresa, 'usuarios': usuarios})


@login_required
def desativar_ativar_empresa(request, pk):
    if request.user.is_superuser:
        empresa = get_object_or_404(Empresa, pk=pk)

        if empresa.ativo == True:
            empresa.ativo = False
            empresa.save()
            messages.success(request, "Empresa desativada com sucesso!")
            return redirect('listar_empresas')
        else:
            empresa.ativo = True
            empresa.save()
            messages.success(request, "Empresa ativada com sucesso!")
            return redirect('listar_empresas')
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('index')

"""
PEGAR EMPRESA E PRODUTOS DO USUARIO LOGADO
usuario_id = request.user.id
empresa = Empresa.objects.filter(empresa__usuario_id=usuario_id)
print(empresa)
produtos = list(Produto.objects.filter(empresa_id=1).values())
print(produtos)
"""
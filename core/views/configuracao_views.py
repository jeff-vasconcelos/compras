from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from core.models.parametros_models import Parametro
from api.models.fornecedor import Fornecedor
from django.contrib.auth.decorators import login_required
from core.forms.fornecedor_forms import FornecedorForm
from core.forms.parametros_form import ParametroForm


@login_required
def configuracao_painel(request, template_name='aplicacao/paginas/configuracao/configuracao.html'):
    empresa = request.user.usuario.empresa
    parametros = Parametro.objects.get(empresa__id=empresa.pk)
    fornecedor = Fornecedor.objects.get(empresa__id=empresa.pk)

    contexto = {
        'parametro': parametros,
        'fornecedor': fornecedor
    }
    return render(request, template_name, contexto)


@login_required
def editar_fornecedor_conf(request, pk, template_name='aplicacao/paginas/configuracao/fornec_edit.html'):
    if request.user.usuario.tipo == "Administrador":
        fornecedor = Fornecedor.objects.get(pk=pk)
        if request.method == 'POST':
            form = FornecedorForm(request.POST, instance=fornecedor)
            if form.is_valid():
                fornecedor = form.save(commit=False)
                fornecedor.save()
                messages.success(request, "Fornecedor atualizado com sucesso!")
                return redirect('configuracao_painel')
            else:
                messages.error(request, "Ops, não foi possivel atualizar")
        else:
            form = FornecedorForm(instance=fornecedor)
        return render(request, template_name, {'form': form, 'fornecedor': fornecedor})
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('index')



@login_required
def editar_parametro_conf(request, pk, template_name='aplicacao/paginas/configuracao/param_edit.html'):
    if request.user.usuario.tipo == "Administrador":
        parametro = Parametro.objects.get(pk=pk)
        if request.method == 'POST':
            form = ParametroForm(request.POST, instance=parametro)
            if form.is_valid():
                parametro = form.save(commit=False)
                parametro.save()
                messages.success(request, "Parametros atualizados com sucesso!")
                return redirect('configuracao_painel')
            else:
                messages.error(request, "Ops, não foi possivel atualizar")
        else:
            form = ParametroForm(instance=parametro)
        return render(request, template_name, {'form': form})
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('index')

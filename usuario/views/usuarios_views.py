from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.core.paginator import Paginator, InvalidPage
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from core.forms.usuarios_form import *
from usuario.models import *


""" Função de Login """
def login_painel(request, template_name="administracao/login.html"):
    next = request.GET.get('next', '/painel/administracao')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff == True:

                if user.is_active == True:
                    login(request, user)
                    messages.success(request, "Login realizado com sucesso!")
                    return HttpResponseRedirect(next)
                else:
                    messages.error(request, "Usuário inativo")
                    return HttpResponseRedirect(settings.LOGIN_URL)

            else:
                messages.error(request, "Usuário não tem permissão")
                return HttpResponseRedirect(settings.LOGIN_URL)

        else:
            messages.error(request, "Email e/ou Senha incorretos.")
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, template_name, {'redirect_to':next})


""" Função de Logout """
def logout_painel(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


""" Acesso a Ferramenta """
@login_required
def painel_administrativo(request, template_name="administracao/painel.html"):
    if request.user.is_staff:
        return render(request, template_name)


""" Acesso ao perfil de administração """
@login_required
def perfil_admin(request, template_name="administracao/usuarios/perfil_admin.html"):
    return render(request, template_name)


""" Editar perfil de administração """
@login_required
def editar_admin(request, template_name="administracao/usuarios/editar_admin.html"):
    #usuario = get_object_or_404(Usuario, pk=request.user.pk)
    user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = UsuarioAdminForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.is_active = True
            user.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('perfil_admin')
    else:
        form = UsuarioAdminForm(instance=user)

    return render(request, template_name, {'form': form})


##### USUÁRIOS - SERVIDORES CBM #####
@login_required
def cadastrar_usuario(request, template_name="administracao/usuarios/cadastro_usuario.html"):
    try:
        form2 = UsuarioForm(request.POST or None)
        form = UsuarioAdminForm(request.POST or None)
        if request.method == "POST":
            password_confirm = request.POST['password_confirm']
            password = request.POST['password']
            tipo = request.POST['tipo']
            admin = "admin"
            if password == password_confirm:
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(user.password)
                    if tipo == admin:
                        user.is_staff = True
                    else:
                        user.is_staff = False
                    user.is_active = True
                    user.save()
                    user2 = User.objects.get(username=user.username)
                    usuario = form2.save(commit=False)
                    usuario.user = user2
                    usuario.save()
                    messages.success(request, "Cadastrado com sucesso!")
                    return redirect('listar_usuarios')
                else:
                    messages.error(request, "Usuário ja existe!")
            else:
                messages.error(request, "Senhas não conferem. Tente novamente!")
    except Exception:
        messages.error(request, "Erro ao cadastrar usuário!")
    return render(request, template_name, {'form': form, 'form2': form2})


@login_required
def listar_usuarios(request, template_name="administracao/usuarios/listar_usuarios.html"):
    if request.user.is_staff:
        usuario = Usuario.objects.all()
        usuarios = {'usuarios':usuario}
        return render(request, template_name, usuarios)
    else:
        messages.error(request, "Vocẽ não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')

@login_required
def remover_usuario(request, pk):
    if request.user.is_staff:
        try:
            usuario = Usuario.objects.get(pk=pk)
            user = User.objects.get(pk=usuario.user.pk)
            usuario.delete()
            user.delete()
            messages.success(request, "Usuario removido com sucesso")
        except Exception:
            messages.error(request, "Não foi possivel remover o usuário")
        return redirect('listar_usuarios')
    else:
        messages.error(request, "Você não tem permissão para acessar a página.")
        return redirect('painel_administrativo')

@login_required
def detalhes_usuario(request, pk, template_name="administracao/usuarios/detalhes_usuario.html"):
    if request.user.is_staff:
        usuario = get_object_or_404(Usuario, pk=pk)
        return render(request, template_name, {'usuario':usuario})
    else:
        messages.error(request, "Você não tem permissão para acessar a página.")
        return redirect('painel_administrativo')


@login_required
def inativar_usuario(request, pk):
    if request.user.is_staff:
        usuario = Usuario.objects.get(pk=pk)
        user = User.objects.get(pk=usuario.user.pk)

        if user.is_active == True:
            user.is_active = False
            user.save()
            messages.success(request, "Usuário inativo!")
            return redirect('listar_usuarios')
        else:
            user.is_active = True
            user.save()
            messages.success(request, "Usuário ativo!")
            return redirect('listar_usuarios')
    else:
        messages.success(request, "Você não tem permissão para acessar a página.")
        return redirect('painel_administrativo')
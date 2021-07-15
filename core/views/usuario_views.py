from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from core.forms.usuarios_forms import *
from core.models.usuarios_models import *


""" Função de Login """
def login_painel(request, template_name="aplicacao/login/login.html"):
    next = request.GET.get('next', '/painel/home')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active == True:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                messages.error(request, "Usuário inativo")
                return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            messages.error(request, "Usuário e/ou Senha incorretos.")
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, template_name, {'redirect_to': next})


""" Função de Logout """
def logout_painel(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


""" Cadastrar usuários """
@login_required
def cadastrar_usuario(request, template_name="aplicacao/paginas/usuarios/usuario_cad.html"):
    if request.user.usuario.tipo == "Administrador":
        try:
            form = UsersForm(request.POST, request.FILES)
            form2 = UsuariosForm(request.POST, request.FILES)
            if request.method == "POST":
                password_confirm = request.POST['password_confirm']
                password = request.POST['password']
                empresa = request.user.usuario.empresa

                if password == password_confirm:
                    if form.is_valid():
                        if form2.is_valid():
                            user = form.save(commit=False)
                            user.set_password(user.password)
                            user.is_active = True
                            user.save()

                            user2 = User.objects.get(username=user.username)
                            usuario = form2.save(commit=False)
                            usuario.usuario = user2
                            usuario.empresa = empresa
                            usuario.save()

                            messages.success(request, "Cadastrado com sucesso!")
                            return redirect('home_painel')
                        else:
                            messages.error(request, "Por favor, verifique os campos obrigatórios!")
                    else:
                        messages.error(request, "Por favor, verifique os campos obrigatórios!")

                else:
                    messages.error(request, "Senhas não conferem. Tente novamente!")
        except Exception:
            messages.error(request, "Erro ao cadastrar usuário, por favor verifique os campos informados!")
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('home_painel')
    return render(request, template_name, {'form': form, 'form2': form2})


""" Função para editar perfil do usuário logado """
@login_required
def editar_perfil(request, template_name="aplicacao/paginas/usuarios/usuario_edit.html"):
    try:
        usuario = get_object_or_404(Usuario, pk=request.user.pk)
        user = get_object_or_404(User, pk=request.user.pk)

        form = UsersForm(request.POST, instance=user)
        form2 = UsuariosForm(request.POST, request.FILES, instance=usuario)

        if request.method == 'POST':

            password_confirm = request.POST['password_confirm']
            password = request.POST['password']

            if password == password_confirm:
                if form.is_valid():
                    if form2.is_valid():
                        user = form.save(commit=False)
                        if user.password != "":
                            user.set_password(user.password)
                        user.is_active = True
                        user.save()

                        usuario = form2.save(commit=False)
                        usuario.save()

                        messages.success(request, "Perfil atualizado com sucesso!")
                        return redirect('login')
                    else:
                        messages.error(request, "Por favor, verifique os campos obrigatórios!")
                else:
                    messages.error(request, "Por favor, verifique os campos obrigatórios!")
            else:
                messages.error(request, "Senhas não conferem. Tente novamente!")
        else:
            form = UsersForm(instance=user)
            form2 = UsuariosForm(instance=usuario)
    except Exception:

        messages.error(request, "Erro ao cadastrar usuário, por favor verifique os campos informados!")
    return render(request, template_name, {'form': form, 'form2': form2})


""" Listando usuários cadastrados """
@login_required
def lista_usuarios(request, template_name="aplicacao/paginas/usuarios/usuarios.html"):
    if request.user.usuario.tipo == "Administrador":
        empresa = request.user.usuario.empresa
        usuario = Usuario.objects.filter(empresa__id=empresa.pk)
        usuarios = {'usuarios': usuario}
        return render(request, template_name, usuarios)
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('home_painel')


""" Função para editar usuário """
@login_required
def editar_usuario(request, pk, template_name="aplicacao/paginas/usuarios/usuario_edit.html"):
    if request.user.usuario.tipo == "Administrador":
        usuario = Usuario.objects.get(pk=pk)
        user = User.objects.get(pk=usuario.pk)

        try:
            if request.method == 'POST':
                form = UsersForm(request.POST, instance=user)
                form2 = UsuariosForm(request.POST, request.FILES, instance=usuario)

                password_confirm = request.POST['password_confirm']
                password = request.POST['password']

                if password == password_confirm:
                    if form.is_valid():
                        if form2.is_valid():
                            user = form.save(commit=False)
                            if user.password != "":
                                user.set_password(user.password)
                            user.is_active = True
                            user.save()

                            usuario = form2.save(commit=False)
                            usuario.save()

                            messages.success(request, "Usuário atualizado com sucesso!")
                            return redirect('listar-usuarios')
                        else:
                            messages.error(request, "Por favor, verifique os campos obrigatórios!")
                    else:
                        messages.error(request, "Por favor, verifique os campos obrigatórios!")
                else:
                    messages.error(request, "Senhas não conferem. Tente novamente!")
            else:
                form = UsersForm(instance=user)
                form2 = UsuariosForm(instance=usuario)
        except Exception:
            messages.error(request, "Erro ao editar usuário, por favor verifique os campos informados!")
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('home_painel')
    return render(request, template_name, {'form': form, 'form2': form2})


""" Inativar usuários """
@login_required
def inativar_usuario(request, pk):
    if request.user.usuario.tipo == "Administrador":
        usuario = Usuario.objects.get(pk=pk)
        user = User.objects.get(pk=usuario.pk)

        if user.is_active == True:
            user.is_active = False
            user.save()
            messages.success(request, "Usuário inativo!")
            return redirect('listar-usuarios')
        else:
            user.is_active = True
            user.save()
            messages.success(request, "Usuário ativo!")
            return redirect('listar-usuarios')
    else:
        messages.error(request, "Ops, o usuário não tem permissão!")
        return redirect('home_painel')
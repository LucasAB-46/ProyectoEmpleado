from django.contrib import messages
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .models import Empleado
from .forms import EmpleadoForm

# Vista principal (Home)
class IndexView(TemplateView):
    template_name = 'empleados/home.html'


# Lista todos los empleados (con filtro por departamento)
class ListarTodosEmpleados(LoginRequiredMixin, ListView):
    model = Empleado
    template_name = 'empleados/empleado_list.html'
    context_object_name = 'empleados'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        departamento = self.request.GET.get('departamento')
        if departamento:
            queryset = queryset.filter(departamento__nombre=departamento)
        return queryset


# Lista empleados por departamento (usando URL parameter)
class ListarEmpleadosPorDepartamento(LoginRequiredMixin, ListView):
    model = Empleado
    template_name = 'empleados/empleado_list.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        nombre_departamento = self.kwargs.get('nombre')
        return Empleado.objects.filter(departamento__nombre=nombre_departamento)


# Detalle de MiModelo
class EmpleadoDetailView(LoginRequiredMixin, DetailView):
    model = Empleado
    template_name = 'empleados/empleado_detail.html'  # Asegúrate de crear este template
    context_object_name = 'empleado'


# Crear empleado (con manejo mejorado de errores)
class EmpleadoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleados/empleado_form.html'
    success_url = reverse_lazy('empleado_list')
    permission_required = 'empleado.add_empleado'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Empleado {self.object} creado exitosamente')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error en {field}: {error}')
        return super().form_invalid(form)


# Actualizar empleado (con manejo mejorado de errores)
class EmpleadoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleados/empleado_form.html'
    success_url = reverse_lazy('empleado_list')
    permission_required = 'empleado.change_empleado'

    def form_valid(self, form):
        messages.success(self.request, f'Empleado {self.object} actualizado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error en {field}: {error}')
        return super().form_invalid(form)


# Eliminar empleado
class EmpleadoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Empleado
    template_name = 'empleados/empleado_confirm_delete.html'
    success_url = reverse_lazy('empleado_list')
    permission_required = 'empleado.delete_empleado'

    def delete(self, request, *args, **kwargs):
        empleado = self.get_object()
        messages.success(request, f'Empleado {empleado} eliminado correctamente')
        return super().delete(request, *args, **kwargs)


# Autenticación
def sessionLogIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciales incorrectas')
    return render(request, 'empleados/login.html')

def sessionLogOut(request):
    logout(request)
    return redirect('login')


# Vistas de prueba (opcionales)
class PruebaListView(ListView):
    model = Empleado
    template_name = 'empleados/prueba_list.html'





    

 

from django.urls import path
from . import views
from django.http import HttpResponse

app_name = 'client'

# Función simple de éxito simulada para la redirección
def claim_success_view(request, pk):
    return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head><title>Éxito</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"></head>
        <body>
            <div class="container text-center py-5">
                <div class="alert alert-success" role="alert">
                    <h4 class="alert-heading">Reclamación Enviada con Éxito!</h4>
                    <p>Su solicitud (ID: <strong>{pk}</strong>) ha sido recibida y está en estado <strong>Pendiente</strong>.</p>
                    <hr>
                    <p class="mb-0">Pronto recibirá notificaciones sobre el estado de su reclamación.</p>
                </div>
                <a href="/" class="btn btn-primary mt-3">Volver a Inicio</a>
            </div>
        </body>
        </html>
    """)

urlpatterns = [
    path('', views.home, name='home'),
    path('solicitations/', views.solicitations, name='solicitations'),
    path('solicitations/<int:pk>/', views.solicitation_details, name='solicitation_details'),
    path('reclamacion/nueva/', views.create_claim_solicitation, name='new_claim'),
    path('reclamacion/exito/<int:pk>/', claim_success_view, name='claim_success'),
]

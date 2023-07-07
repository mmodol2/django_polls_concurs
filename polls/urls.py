from django.urls import path
from .views import obtener_datos_grafica

from . import views
from .views import DatosGraficaAPIView

app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("concurs/", views.ConcursView.as_view(), name="concurs"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('question/<int:question_id>/obtener-datos-grafica/', obtener_datos_grafica, name='obtener_datos_grafica'),
    path('api/question/<int:pk>/datos-grafica/', DatosGraficaAPIView.as_view(), name='datos_grafica_api'),
]

# urlpatterns = [    
#     # ex: /polls/
#     path("", views.index, name="index"),
#     # ex: /polls/5/
#     path("<int:question_id>/", views.detail, name="detail"),
#     # ex: /polls/5/results/
#     path("<int:question_id>/results/", views.results, name="results"),
#     # ex: /polls/5/vote/
#     path("<int:question_id>/vote/", views.vote, name="vote"),
# ]
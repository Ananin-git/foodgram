from api.views import redirect_to_recipe
from django.urls import path

urlpatterns = [
    path('<int:pk>/', redirect_to_recipe, name='short-link'),
]

from django.urls import path
from .views import MyModelListView, MyModelCreateView, MyModelUpdateView, MyModelDeleteView

urlpatterns = [
    path('', MyModelListView.as_view(), name='my_model_list'),
    path('create/', MyModelCreateView.as_view(), name='my_model_create'),
    path('<int:pk>/update/', MyModelUpdateView.as_view(), name='my_model_update'),
    path('<int:pk>/delete/', MyModelDeleteView.as_view(), name='my_model_delete'),
]

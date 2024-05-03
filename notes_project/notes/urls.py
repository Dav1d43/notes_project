from django.urls import path
from .views import MyModelListView, MyModelCreateView

urlpatterns = [
    path('', MyModelListView.as_view(), name='my_model_list'),
    path('create/', MyModelCreateView.as_view(), name='my_model_create'),

]

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import MyModel
from .forms import MyModelForm

class MyModelListView(ListView):
    model = MyModel
    template_name = 'myapp/model_list.html'

    def get_queryset(self):
        return MyModel.objects.all()

class MyModelCreateView(CreateView):
    model = MyModel
    form_class = MyModelForm
    template_name = 'myapp/model_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

from django.test import TestCase
from django.urls import reverse
from .models import MyModel, Category
from .forms import MyModelForm
from django.contrib.auth.models import User


class MyModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')
        self.obj = MyModel.objects.create(user=self.user, category=self.category, title="Test Title",
                                          content="Test Content")

    def test_model_can_be_saved(self):
        self.assertEqual(MyModel.objects.count(), 1)

    def test_model_can_be_retrieved(self):
        obj = MyModel.objects.get(title="Test Title")
        self.assertEqual(obj, self.obj)

    def test_model_can_be_updated(self):
        self.obj.title = "Updated Test Title"
        self.obj.save()
        obj = MyModel.objects.get(content="Test Content")
        self.assertEqual(obj.title, "Updated Test Title")

    def test_model_can_be_deleted(self):
        self.obj.delete()
        self.assertEqual(MyModel.objects.count(), 0)


class MyModelListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')
        self.obj = MyModel.objects.create(user=self.user, category=self.category, title="Test Title",
                                          content="Test Content")

    def test_list_view_status_code(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('my_model_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_queryset(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('my_model_list'))
        self.assertQuerysetEqual(response.context['object_list'], ['<MyModel: Test Title>'])

    def test_list_view_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('my_model_list'))
        self.assertTemplateUsed(response, 'myapp/model_list.html')


class MyModelFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')

    def test_valid_form(self):
        form_data = {'category': self.category.id, 'title': 'Test Title', 'content': 'Test Content'}
        form = MyModelForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'category': '', 'title': '', 'content': ''}
        form = MyModelForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())


class MyModelUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')
        self.obj = MyModel.objects.create(user=self.user, category=self.category, title="Test Title",
                                          content="Test Content")

    def test_update_view_status_code(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('my_model_update', kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, 200)

    def test_update_view_updates_object_correctly(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('my_model_update', kwargs={'pk': self.obj.pk}),
                                    {'category': self.category.id, 'title': 'Updated Test Title',
                                     'content': 'Updated Test Content'})
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.title, 'Updated Test Title')

    def test_update_view_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('my_model_update', kwargs={'pk': self.obj.pk}))
        self.assertTemplateUsed(response, 'myapp/model_form.html')


class MyModelDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')
        self.obj = MyModel.objects.create(user=self.user, category=self.category, title="Test Title",
                                          content="Test Content")

    def test_delete_view_status_code(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('my_model_delete', kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, 302)

    def test_delete_view_deletes_object_correctly(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('my_model_delete', kwargs={'pk': self.obj.pk}))
        self.assertEqual(MyModel.objects.count(), 0)

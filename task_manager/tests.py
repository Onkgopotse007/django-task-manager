from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            priority='High',
            due_date='2024-02-20',
            status='Pending',
            user=self.user
        )

    def test_task_creation(self):
        self.assertEqual(Task.objects.count(), 1)

    def test_task_editing(self):
        edit_url = reverse('task_edit', kwargs={'task_id': self.task.id})
        response = self.client.post(edit_url, {
            'title': 'Updated Task',
            'description': 'This is an updated test task',
            'priority': 'Low',
            'due_date': '2024-02-21',
            'status': 'Completed',
        })
        self.assertEqual(response.status_code, 302)  # Check if redirect happens after task editing
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_task_deletion(self):
        delete_url = reverse('task_delete', kwargs={'task_id': self.task.id})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)  # Check if redirect happens after task deletion
        self.assertEqual(Task.objects.count(), 0)


class TaskFormTest(TestCase):
    def test_valid_due_date(self):
        form_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'priority': 'High',
            'due_date': '2024-02-20',
            'status': 'Pending',
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_past_due_date(self):
        form_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'priority': 'High',
            'due_date': '2023-02-20',  # Past date
            'status': 'Pending',
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['due_date'], ['Due date must be in the future'])


class UserAuthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_user_signup(self):
        signup_url = reverse('signup')
        response = self.client.post(signup_url, {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertEqual(response.status_code, 302)  # Check if redirect happens after signup
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        login_url = reverse('login')
        response = self.client.post(login_url, {
            'username': 'testuser',
            'password': '12345',
        })
        self.assertEqual(response.status_code, 302)  # Check if redirect happens after login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_logout(self):
        self.client.login(username='testuser', password='12345')
        logout_url = reverse('logout')
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, 302)  # Check if redirect happens after logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)

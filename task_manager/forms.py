from django import forms
from django.utils import timezone

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'status']

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date < timezone.now().date():
            raise forms.ValidationError("Due date must be in the future")
        return due_date

from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What\'s your question?',
                'maxlength': '200'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your question in detail...',
                'rows': 4
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'title': 'Question Title',
            'content': 'Question Details',
            'image': 'Upload Image (Optional)'
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your answer...',
                'rows': 3
            })
        }
        labels = {
            'content': 'Your Answer'
        }
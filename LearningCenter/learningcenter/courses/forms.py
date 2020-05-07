from django import forms


class MessageForm(forms.Form):
    email = forms.EmailField(label='Почта для обратной связи', max_length=100,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(label='Заголовок', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'form-control'}))

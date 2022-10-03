from django import forms

class UsersForm(ModelForm):
	password = forms.CharField(widget=PasswordInput)

    class Meta:
        model = Users
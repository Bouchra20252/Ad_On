from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    UserProfile, Advertisement, Category, AdImage, 
    Message, AdComment, SavedSearch, Report
)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'postal_code', 'bio', 'image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

class AdvertisementForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'price', 'negotiable', 'category', 'location']
        widgets = {
            'negotiable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-select'})
        }

class AdImageForm(forms.ModelForm):
    class Meta:
        model = AdImage
        fields = ['image', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class AdImageFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        primary_count = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_primary'):
                    primary_count += 1
        
        if primary_count > 1:
            raise forms.ValidationError("Vous ne pouvez avoir qu'une seule image principale.")
        elif self.total_form_count() > 0 and primary_count == 0:
            raise forms.ValidationError("Vous devez désigner une image principale.")

AdImageFormSet = forms.inlineformset_factory(
    Advertisement, AdImage, form=AdImageForm, formset=AdImageFormSet,
    extra=3, max_num=10, validate_max=True, can_delete=True
)

class MessageForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.HiddenInput(), required=False)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    
    class Meta:
        model = Message
        fields = ['subject', 'content']

class AdCommentForm(forms.ModelForm):
    content = forms.CharField(
        label='Question',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Posez votre question sur cette annonce...'
        })
    )
    
    class Meta:
        model = AdComment
        fields = ['content']

class SearchForm(forms.Form):
    q = forms.CharField(
        label='Recherche',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Que recherchez-vous ?'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Toutes les catégories",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(
        label='Prix min',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min'
        })
    )
    max_price = forms.DecimalField(
        label='Prix max',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max'
        })
    )
    location = forms.CharField(
        label='Localisation',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ville, département...'
        })
    )

class SavedSearchForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nom de votre recherche'
    }))
    
    class Meta:
        model = SavedSearch
        fields = ['name', 'category', 'min_price', 'max_price', 'location', 'send_notifications']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'min_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'send_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class ReportForm(forms.ModelForm):
    details = forms.CharField(
        label='Détails',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Décrivez pourquoi vous signalez cette annonce...'
        })
    )
    
    class Meta:
        model = Report
        fields = ['report_type', 'details']
        widgets = {
            'report_type': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'report_type': 'Motif du signalement'
        } 
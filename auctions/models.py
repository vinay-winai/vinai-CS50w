from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.forms import ModelForm,Textarea,TextInput,NumberInput,Select,HiddenInput

class User(AbstractUser):
    email = models.EmailField(blank=False)
    
    REQUIRED_FIELDS = ['email']

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(max_length=256, blank=False)
    img = models.URLField(blank=True)
    base_bid = models.FloatField(blank=False,validators=[MinValueValidator(0.0),MaxValueValidator(99999999.99)])
    watch_list = models.ManyToManyField(User, blank=True, related_name="user_watchlist")
    category = models.ForeignKey(Category, on_delete=models.CASCADE , blank=True, null= True )
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    new_bid = models.FloatField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=128)

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ['watch_list']
        widgets = {
            'title': TextInput(attrs={'placeholder':'Enter title',
        'class': 'form-control col-md-10 col-lg-10'}),
        'description': Textarea(attrs={'placeholder':'Type about the product',
        'class': 'form-control col-md-10 col-lg-10','rows':4}),
        'img': TextInput(attrs={'placeholder':'Enter title',
        'class': 'form-control col-md-10 col-lg-10'}),
        'base_bid': NumberInput(attrs={'placeholder':'Enter the base price',
        'class': 'form-control col-sm-6 col-md-4 col-lg-3'}),
        'category': Select(attrs={'placeholder':'Enter title',
        'class': 'form-control col-sm-6 col-md-4 col-lg-3'}),
        'user': HiddenInput(),

        }

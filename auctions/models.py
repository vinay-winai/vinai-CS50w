from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.forms import ModelForm,Textarea,TextInput,NumberInput,Select,HiddenInput

class User(AbstractUser):
    email = models.EmailField(max_length=64)

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=256)
    img = models.CharField(blank=True,max_length=256)
    curr_bid = models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(99999999.99)])
    watch_list = models.ManyToManyField(User, blank=True, related_name="listings")
    category = models.ForeignKey(Category, on_delete=models.CASCADE , blank=True, null= True )
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    new_bid = models.FloatField()

class Comment(models.Model):
    user = models.ForeignKey(User,default=9 , on_delete=models.SET_DEFAULT, null=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=128)

class ListingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['curr_bid'].label = "Base price"
    class Meta:
        model = Listing
        exclude = ['watch_list','is_active']
        widgets = {
            'title': TextInput(attrs={'placeholder':'Enter title',
        'class': 'form-control col-md-10 col-lg-10'}),
        'description': Textarea(attrs={'placeholder':'Type about the product',
        'class': 'form-control col-md-10 col-lg-10','rows':4}),
        'img': TextInput(attrs={'placeholder':'Submit an img URL',
        'class': 'form-control col-md-10 col-lg-10'}),
        'curr_bid': NumberInput(attrs={'placeholder':'Enter the base price',
        'class': 'form-control col-sm-6 col-md-4 col-lg-3'}),
        'category': Select(attrs={'class': 'form-control col-sm-6 col-md-4 col-lg-3'}),
        'user': HiddenInput()
        }
            
class BidForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_bid'].label = ""
    class Meta:
        model = Bid
        fields = '__all__'
        widgets = {
            'new_bid': NumberInput(attrs={'placeholder':'Enter price higher than above',
        'class': 'form-control col-8 col-md-4 col-lg-3'}),
        'user': HiddenInput(),
        'item': HiddenInput(),
        }

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].label = ""
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {
        'user': HiddenInput(),
        'item': HiddenInput(),
        'comment': Textarea(attrs={'placeholder':'Comment here',
        'class': 'form-control col-md-10 col-lg-10','rows':2}),
        }
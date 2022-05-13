from django.db import models

class Post(models.Model):
    rare_user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    publication_date = models.DateField(auto_now=True)
    image_url = models.TextField()
    content = models.TextField()
    approved = models.BooleanField()
    tags = models.ManyToManyField(
        'Tag',
        through = 'postTag',
        related_name= 'posts'
    )

    
    
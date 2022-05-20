from django.db import models

from rareapi.models.post import Post


class Subscription(models.Model):
    follower = models.ForeignKey(
        "RareUser", on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(
        "RareUser", on_delete=models.CASCADE, related_name="author")
    created_on = models.DateField(auto_now=True)
    ended_on = models.DateField(null=True)
    
    # self is representing instance of sub
    @property 
    def posts(self):
        # filter post ove author ID
        # left side of filter is column name in the table we are filtering(POST)
        author_posts = Post.objects.filter(rare_user=self.author)
        # author_posts become su.post value
        return author_posts

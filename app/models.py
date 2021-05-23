from django.db import models
from django.contrib.humanize.templatetags import humanize

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='images/')
    bio = models.TextField(blank=True, null=True)
    following = models.ManyToManyField(
        'self', related_name='followers', symmetrical=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} {self.email}'
    
    def get_ordered_posts(self):
        return self.post_set.order_by('-created_at')


class Location(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    text = models.TextField()
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_liked(self, u):
        print(self.like_set.filter(user=u))
        return True

    def get_created_at(self):
        return humanize.naturaltime(self.created_at)

    def __str__(self):
        return f'{self.user} {self.created_at}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} {self.post} {self.created_at}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.post} {self.created_at}'

    def get_created_at(self):
        return humanize.naturaltime(self.created_at)


class NotificationType(models.IntegerChoices):
    FOLLOW = 1
    COMMENT = 2
    LIKE = 3


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    notification_type = models.IntegerField(choices=NotificationType.choices)
    inicializer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="inicializer")
    post = models.ForeignKey(Post, blank=True,
                             null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, blank=True,
                                null=True, on_delete=models.CASCADE)
    like = models.ForeignKey(Like, blank=True,
                             null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.notification_type} {self.created_at}'

    def get_created_at(self):
        return humanize.naturaltime(self.created_at)

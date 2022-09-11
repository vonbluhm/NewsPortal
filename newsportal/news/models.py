from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        posts = self.post_set.aggregate(rating=Sum('rating'))
        pR = 0
        pR += posts.get('rating')

        comments = self.user.comment_set.aggregate(rating=Sum('rating'))
        cR = 0
        cR += comments.get('rating')
        self.ratingAuthor = pR * 3 + cR
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    regular_article = 'R'
    news_article = 'N'
    TYPES = [
        (regular_article, 'Article'),
        (news_article, 'News')
    ]
    type = models.CharField(max_length=1, choices=TYPES, default=regular_article)

    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(str(self.text)) > 124:
            return f'{self.text[:124]}...'
        else:
            return f'{self.text}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dt = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

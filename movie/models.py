from django.db import models

# Modelo existente Movie (mantenlo como está)
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.URLField()
    url = models.URLField(blank=True)
    year = models.IntegerField()
    genre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title

# Nuevo modelo para Newsletter
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['-subscribed_date']
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
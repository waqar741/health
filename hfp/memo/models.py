# from django.db import models
# from django.contrib.auth.models import User

# class Memo(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField(max_length=2000)
#     photo = models.ImageField(upload_to='photos/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f'Memory by {self.user.username}-{self.text[:10]} at {self.created_at}'
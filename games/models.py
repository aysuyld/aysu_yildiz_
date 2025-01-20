from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, verbose_name="Biyografi")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Profil Fotoğrafı")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Konum")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Doğum Tarihi")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_level = models.IntegerField(default=1)
    stars = models.IntegerField(default=0)
    completed_levels = models.JSONField(default=list)
    last_played = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kullanıcı İlerlemesi"
        verbose_name_plural = "Kullanıcı İlerlemeleri"

class UserCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField()
    code = models.TextField()
    is_completed = models.BooleanField(default=False)
    steps_used = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kullanıcı Kodu"
        verbose_name_plural = "Kullanıcı Kodları"
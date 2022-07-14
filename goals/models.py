from django.db import models


class Aim(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=False)

    def __str__(self):
        return self.name


class Dream(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def dream_to_aim(self, deadline):
        aim = Aim.objects.create(
            name=self.name,
            user=self.user,
            description=self.description,
            created_at=self.created_at,
            deadline=deadline,
        )
        self.delete()
        return aim


class Note(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey("user.User", on_delete=models.CASCADE)
    video = models.FileField(upload_to="uploads/videos/", blank=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Todo
class Todo(models.Model):
    """
    Todo Model to store data
    - title ,description and deadline
    - order by complete ,deadline
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(null=False, blank=False, max_length=50)
    desc = models.TextField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    complete = models.BooleanField(default=False)

    class Meta:
        ordering = ["complete", "deadline"]

    def __str__(self) -> str:
        return self.title

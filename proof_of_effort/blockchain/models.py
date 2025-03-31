from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('student', 'Student'),
    ('validator', 'Validator'),
    ('admin', 'Admin')
]

class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    public_key = models.TextField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class TokenLedger(models.Model):
    user = models.ForeignKey(UserWallet, on_delete=models.CASCADE, related_name="transactions")
    amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    source_block_index = models.IntegerField()
    reason = models.CharField(max_length=255, default="Effort reward")

    def __str__(self):
        return f"{self.user.user.username} earned {self.amount} EFF (block #{self.source_block_index})"

admin.site.register(UserWallet)
admin.site.register(TokenLedger)
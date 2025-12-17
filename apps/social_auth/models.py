from django.db import models


class SocialAccount(models.Model):
    """Social media accounts"""
    account_type = models.CharField(max_length=50, choices=(
        ('FACEBOOK', 'Facebook'),
        ('TWITTER', 'Twitter'),
        ('INSTAGRAM', 'Instagram'),
        ('LINKEDIN', 'LinkedIn'),
        ('YOUTUBE', 'YouTube'),
        ('TIKTOK', 'TikTok'),
    ))
    account_handle = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    follower_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.account_type} - {self.account_handle}"


class SocialApplicationToken(models.Model):
    """Social application access tokens"""
    app_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=50)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500, blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.app_name} - {self.account_type}"


class SocialApplication(models.Model):
    """Social media applications"""
    app_name = models.CharField(max_length=255, unique=True)
    app_type = models.CharField(max_length=50)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    api_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.app_name

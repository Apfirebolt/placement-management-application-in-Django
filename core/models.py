from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from placement_management.settings import AUTH_USER_MODEL


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True, max_length=255)
    username = models.CharField("User Name", unique=True, max_length=255, blank=True, null=True)
    firstName = models.CharField("First Name", max_length=100, blank=True, null=True)
    lastName = models.CharField("Last Name", max_length=100, blank=True, null=True)
    profile_image = models.FileField(upload_to='profile_image', blank=True, null=True)
    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Staff', default=False)
    is_superuser = models.BooleanField('Super User', default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        '''Doc string for meta'''
        verbose_name_plural = "User"


class Company(models.Model):
    name = models.CharField(max_length=255)
    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='companies_added')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.name) + ' - ' + str(self.user_id.email)

    class Meta:
        verbose_name_plural = "Companies"


class Question(models.Model):
    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions_posted')
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_user_questions')
    content = models.TextField("Question Text")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '(%s, %s)' % (self.user_id.email, self.company_id.name)

    class Meta:
        verbose_name_plural = "User Company Questions"


class Application(models.Model):
    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_applications')
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_user_applications')
    notes = models.TextField("Additional Notes")
    source = models.CharField("Source", max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '(%s, %s)' % (self.user_id.email, self.company_id.name)

    class Meta:
        verbose_name_plural = "User Company Applications"

class Interview(models.Model):
    application_id = models.ForeignKey(Application, on_delete=models.CASCADE)
    notes = models.TextField("Additional Notes")
    round = models.CharField("Interview Round/Stage", max_length=255, null=True, blank=True)
    scheduled_at = models.DateTimeField()
    result = models.CharField("Interview Result", max_length=50, null=True, blank=True)

    def __str__(self):
        return '(%s, %s)' % (self.application_id, self.result)

    class Meta:
        verbose_name_plural = "Interviews"

class Offer(models.Model):
    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    notes = models.TextField("Additional Notes", blank=True, null=True)
    ctc = models.CharField("CTC Break UP", max_length=255, null=True, blank=True)
    received_at = models.DateTimeField()
    is_accepted = models.BooleanField("Offer Accepted", default=False)

    def __str__(self):
        return '(%s, %s)' % (self.user_id, self.company_id)

    class Meta:
        verbose_name_plural = "Offers"


class Resume(models.Model):
    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_resumes')
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_resumes')
    resume = models.ImageField("Resume", upload_to='resumes')
    

    def __str__(self):
        return '(%s, %s)' % (self.user_id, self.company_id)

    class Meta:
        verbose_name_plural = "Resumes"








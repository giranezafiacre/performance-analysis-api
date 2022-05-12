from django.urls import reverse
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, fullname, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            fullname=fullname,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            fullname=fullname,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    fullname = models.CharField(max_length=30, null=False)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    approved = models.BooleanField(default=False)
    role_select=(
        ('1', 'registrar'),
        ('2', 'faculty'),
    )
    role = models.CharField(max_length=25, choices=role_select,blank=True,null=True)

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
    objects = UserManager()


class File(models.Model):
    File_name = models.CharField(
        max_length=100, help_text='enter file name', unique=True)
    Actual_file = models.FileField(
        upload_to='app/uploads/', help_text='upload file in csv format')

    def __str__(self):
        """String for representing the Model object."""
        return self.Actual_file

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('file-detail', args=[str(self.id)])


class Student(models.Model):
    fname = models.CharField(max_length=30, null=False)
    gender_select = (
        ('1', 'male'),
        ('2', 'female'),
    )
    gender = models.CharField(max_length=25, choices=gender_select)
    health_select = (
        ('1', 'normal'),
        ('2', 'chronic_disease'),
        ('3', 'disability'),
    )
    healthStatus = models.CharField(max_length=25, choices=health_select)
    program_select = (
        ('1', 'day'),
        ('2', 'evening'),
    )
    program = models.CharField(max_length=25, choices=program_select)
    backId = models.ForeignKey(
        'BackgroundStudy', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        """String for representing the Model object."""
        return self.fname


class BackgroundStudy(models.Model):
    major = models.CharField(max_length=5, null=False)
    school = models.CharField(max_length=60, null=False)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.school

class Course(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class CourseGroup(models.Model):
    groupname = models.CharField(max_length=30, null=False)
    course= models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(
        'Teacher', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.groupname} {self.course}'

class Teacher(models.Model):
    teacherName = models.CharField(max_length=30, null=False)
    def __str__(self):
        """String for representing the Model object."""
        return self.teacherName

class Registration(models.Model):
    student= models.ForeignKey(Student,on_delete=models.SET_NULL, null=True)
    courseGroup = models.ForeignKey(CourseGroup,on_delete=models.SET_NULL, null=True)

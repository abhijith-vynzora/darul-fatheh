from django.db import models
from django.utils import timezone
from utils.image_optimizer import optimize_image
from django.utils.text import slugify

class OptimizedImageModel(models.Model):
    image_fields = []  

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        for field in self.image_fields:
            image_field = getattr(self, field, None)
            if image_field and hasattr(image_field, "path"):
                optimize_image(image_field.path)


class ManagementTeam(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = [ 'name']
        verbose_name = 'Management Team Member'
        verbose_name_plural = 'Management Team'
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name="Detailed Description")
    duration = models.CharField(max_length=100)
    instructor = models.CharField(max_length=200,blank=True)
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date']
        verbose_name_plural = 'News'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title





class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class GalleryImage(OptimizedImageModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="images"
    )
    title = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to="gallery/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    image_fields = ["image"]

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"


class DonationDetails(models.Model):
    donor_name = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    donated_at = models.DateTimeField(auto_now_add=True)
    screenshot = models.ImageField(upload_to='donation_proofs/', blank=True, null=True)
    
    class Meta:
        ordering = ['-donated_at']
        verbose_name_plural = 'Donation Details'
    
    def __str__(self):
        return f"{self.donor_name} - ${self.amount}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


# class Download(models.Model):
#     CATEGORY_CHOICES = [
#         ('syllabus', 'Syllabus'),
#         ('form', 'Form'),
#         ('brochure', 'Brochure'),
#         ('document', 'Document'),
#         ('other', 'Other'),
#     ]
    
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='document')
#     file = models.FileField(upload_to='downloads/')
#     file_size = models.CharField(max_length=50, blank=True)
#     download_count = models.IntegerField(default=0)
#     is_active = models.BooleanField(default=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         ordering = ['-uploaded_at']
    
#     def __str__(self):
#         return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    content = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.IntegerField(default=5)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.designation}"
    

class StudentRegistration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(verbose_name="Date of Birth")
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True) 
    
    program_name = models.CharField(
        max_length=200, 
        verbose_name="Specific Program Name", 
        help_text="e.g. MA English, B.Com, etc."
    )
    
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class AlumniProfile(OptimizedImageModel):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='alumni/photos/')
    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    image_fields = ["photo"] 

    def __str__(self):
        return self.name

class AlumniEvent(OptimizedImageModel):
    event_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='alumni/events/')
    date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True) 

    image_fields = ["image"]

    def __str__(self):
        return self.event_name
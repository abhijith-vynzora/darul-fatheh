from django.db import models
from django.utils import timezone
from utils.image_optimizer import optimize_image
from django.utils.text import slugify

class OptimizedImageModel(models.Model):
    """
    Base class: any model inheriting this can declare image_fields = []
    to auto-optimize images on save.
    """
    image_fields = []  # override in child models

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Optimize all declared image fields
        for field in self.image_fields:
            image_field = getattr(self, field, None)
            if image_field and hasattr(image_field, "path"):
                optimize_image(image_field.path)


class ManagementTeam(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Management Team Member'
        verbose_name_plural = 'Management Team'
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    
    
    # NEW: Short description for the Card View
    short_description = models.TextField(blank=True, help_text="Short summary for the course card (approx. 1-2 sentences).")
    
    # EXISTING: This effectively becomes your "Detailed Description"
    description = models.TextField(verbose_name="Detailed Description")
    
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration = models.CharField(max_length=100)
    instructor = models.CharField(max_length=200,blank=True)
    # fee = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
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
    author = models.CharField(max_length=100)
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


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    organizer = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-event_date']
    
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

    # Tell base model which images to optimize
    image_fields = ["image"]

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"


class DonationDetails(models.Model):
    donor_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # purpose = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    donated_at = models.DateTimeField(auto_now_add=True)
    
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
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class Download(models.Model):
    CATEGORY_CHOICES = [
        ('syllabus', 'Syllabus'),
        ('form', 'Form'),
        ('brochure', 'Brochure'),
        ('document', 'Document'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='document')
    file = models.FileField(upload_to='downloads/')
    file_size = models.CharField(max_length=50, blank=True)
    download_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title


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
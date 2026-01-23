# from django.contrib import admin

# # Import only the models that exist in your models.py
# try:
#     from .models import ManagementTeam
#     @admin.register(ManagementTeam)
#     class ManagementTeamAdmin(admin.ModelAdmin):
#         list_display = ['name', 'position']
#         search_fields = ['name', 'position']
#         list_filter = ['position']
#         ordering = ['position']
# except ImportError:
#     pass

# try:
#     from .models import Course
#     @admin.register(Course)
#     class CourseAdmin(admin.ModelAdmin):
#         list_display = ['title',]
#         search_fields = ['title']
#         # list_filter = ['level', 'is_active']
#         # ordering = ['-created_at']
# except ImportError:
#     pass

# try:
#     from .models import News
#     @admin.register(News)
#     class NewsAdmin(admin.ModelAdmin):
#         list_display = ['title', 'published_date', 'is_published']
#         search_fields = ['title', 'content']
#         list_filter = ['is_published', 'published_date']
#         ordering = ['-published_date']
# except ImportError:
#     pass

# # try:
# #     from .models import Event
# #     @admin.register(Event)
# #     class EventAdmin(admin.ModelAdmin):
# #         list_display = ['title', 'location', 'event_date', 'organizer', 'is_active']
# #         search_fields = ['title', 'location', 'organizer']
# #         list_filter = ['is_active', 'event_date']
# #         ordering = ['-event_date']
# # except ImportError:
# #     pass

# try:
#     from .models import PhotoAlbum
#     @admin.register(PhotoAlbum)
#     class PhotoAlbumAdmin(admin.ModelAdmin):
#         list_display = ['title', 'created_at']
#         search_fields = ['title']
#         list_filter = ['created_at']
#         ordering = ['-created_at']
# except ImportError:
#     pass

# try:
#     from .models import Photo
#     @admin.register(Photo)
#     class PhotoAdmin(admin.ModelAdmin):
#         list_display = ['album', 'uploaded_at']
#         search_fields = [ 'album__title']
#         list_filter = ['uploaded_at', 'album']
#         ordering = ['-uploaded_at']
# except ImportError:
#     pass

# try:
#     from .models import ContactMessage
#     @admin.register(ContactMessage)
#     class ContactMessageAdmin(admin.ModelAdmin):
#         list_display = ['name', 'email', 'subject', 'created_at']
#         search_fields = ['name', 'email', 'subject', 'message']
#         list_filter = [ 'created_at']
#         ordering = ['-created_at']
# except ImportError:
#     pass

# # try:
# #     from .models import Download
# #     @admin.register(Download)
# #     class DownloadAdmin(admin.ModelAdmin):
# #         list_display = ['title', 'category', 'file_size', 'download_count', 'uploaded_at']
# #         search_fields = ['title', 'description']
# #         list_filter = ['category', 'uploaded_at']
# #         ordering = ['-uploaded_at']
# # except ImportError:
# #     pass

# try:
#     from .models import Testimonial
#     @admin.register(Testimonial)
#     class TestimonialAdmin(admin.ModelAdmin):
#         list_display = ['name', 'designation', 'rating', 'is_approved', 'created_at']
#         search_fields = ['name', 'designation', 'content']
#         list_filter = ['rating', 'is_approved', 'created_at']
#         ordering = ['-created_at']
# except ImportError:
#     pass

# # Check if Donation or Donations exists
# try:
#     from .models import Donation
#     @admin.register(Donation)
#     class DonationAdmin(admin.ModelAdmin):
#         list_display = ['donor_name', 'amount',  'payment_method', 'donated_at']
#         search_fields = ['donor_name', 'email', 'transaction_id']
#         list_filter = ['payment_method', 'donated_at']
#         ordering = ['-donated_at']
# except ImportError:
#     try:
#         from .models import Donations
#         @admin.register(Donations)
#         class DonationsAdmin(admin.ModelAdmin):
#             list_display = ['donor_name', 'amount', 'payment_method', 'donated_at']
#             search_fields = ['donor_name', 'email', 'transaction_id']
#             list_filter = ['payment_method', 'donated_at']
#             ordering = ['-donated_at']
#     except ImportError:
#         pass
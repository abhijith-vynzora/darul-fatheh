from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # ==================== PUBLIC WEBSITE URLs (Frontend) ====================
    path('', views.index, name='index'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('faq/', views.faq_page, name='faq'),
    path('prayer-time/', views.prayer_time, name='prayer_time'),
    
    # Courses
    path('courses/', views.courses_page, name='courses'),
    path('course_detail/<slug:slug>/', views.course_detail, name='course_detail'),
    
    # Services
    path('services/', views.services_page, name='services'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    
    # Blog / News
    path('blog/', views.blog_page, name='blog'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),

    #Not found 
    path('not-found/', views.not_found_page, name='not-found'),

    # Gallery
    path('gallery/', views.gallery_page, name='gallery'),

    # Donate
    path('donate/', views.donate, name='donate'), 

    # ==================== ADMIN DASHBOARD URLs (Backend) ====================
    # Authentication
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/login/', views.login_view, name='login'),
    path('dashboard/logout/', views.logout_view, name='logout'),
    
    # Management Team URLs
    path('dashboard/team/', views.team_list, name='team_list'),
    path('dashboard/team/create/', views.team_create, name='team_create'),
    path('dashboard/team/<int:pk>/edit/', views.team_edit, name='team_edit'),
    path('dashboard/team/<int:pk>/delete/', views.team_delete, name='team_delete'),
    
    # Courses URLs (Admin Side)
    path('dashboard/courses/', views.course_list, name='course_list'),
    path('dashboard/courses/create/', views.course_create, name='course_create'),
    path('dashboard/courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('dashboard/courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    
    # News URLs (Admin Side)
    path('dashboard/news/', views.news_list, name='news_list'),
    path('dashboard/news/create/', views.news_create, name='news_create'),
    path('dashboard/news/<int:pk>/edit/', views.news_edit, name='news_edit'),
    path('dashboard/news/<int:pk>/delete/', views.news_delete, name='news_delete'),
    
    # Photo Gallery URLs
    path("dashboard/categories/", views.category_list, name="category_list"),
    path("dashboard/categories/add/", views.add_category, name="add_category"),
    path("dashboard/categories/update/<int:pk>/", views.update_category, name="update_category"),
    path("dashboard/categories/delete/<int:pk>/", views.delete_category, name="delete_category"),
    path("dashboard/list-images/", views.gallery_images, name="list_image"),
    path("dashboard/add_image/", views.add_image, name="add_image"),
    path("dashboard/delete-image/<int:image_id>/", views.delete_image, name="delete_image"),

    # Donations URLs
    path('dashboard/donations/', views.donation_list, name='donation_list'),
    path('dashboard/donations/create/', views.donation_create, name='donation_create'),
    path('dashboard/donations/<int:pk>/edit/', views.donation_edit, name='donation_edit'),
    path('dashboard/donations/<int:pk>/delete/', views.donation_delete, name='donation_delete'),
    
    # Contact Messages URLs
    path('dashboard/messages/', views.message_list, name='message_list'),
    path('dashboard/messages/<int:pk>/view/', views.message_view, name='message_view'),
    path('dashboard/messages/<int:pk>/delete/', views.message_delete, name='message_delete'),
    
    # # Downloads URLs
    # path('dashboard/downloads/', views.download_list, name='download_list'),
    # path('dashboard/downloads/create/', views.download_create, name='download_create'),
    # path('dashboard/downloads/<int:pk>/edit/', views.download_edit, name='download_edit'),
    # path('dashboard/downloads/<int:pk>/delete/', views.download_delete, name='download_delete'),
    
    # Testimonials URLs
    path('dashboard/testimonials/', views.testimonial_list, name='testimonial_list'),
    path('dashboard/testimonials/create/', views.testimonial_create, name='testimonial_create'),
    path('dashboard/testimonials/<int:pk>/edit/', views.testimonial_edit, name='testimonial_edit'),
    path('dashboard/testimonials/<int:pk>/delete/', views.testimonial_delete, name='testimonial_delete'),

    path('our-team/', views.our_team, name='team'),




    # Public URLs
    path('register/', views.register_view, name='register'),

    # Admin Dashboard URLs
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),


    # Alumni Profile Management
    path('alumni/list/', views.alumni_list, name='alumni_list'), 
    path('alumni/create/', views.alumni_create, name='alumni_create'),
    path('alumni/<int:pk>/edit/', views.alumni_edit, name='alumni_edit'),
    path('alumni/<int:pk>/delete/', views.alumni_delete, name='alumni_delete'),

    # Alumni Event Management
    path('alumni-events/', views.alumni_event_list, name='alumni_event_list'),
    path('alumni-events/create/', views.alumni_event_create, name='alumni_event_create'),
    path('alumni-events/<int:pk>/edit/', views.alumni_event_edit, name='alumni_event_edit'),
    path('alumni-events/<int:pk>/delete/', views.alumni_event_delete, name='alumni_event_delete'),

    #public alumni page
    path('alumni/', views.alumni_public_view, name='alumni_page'),
    path('contact/', views.contact_page, name='contact_page'),

]

handler404 = 'admin_panel.views.page404',

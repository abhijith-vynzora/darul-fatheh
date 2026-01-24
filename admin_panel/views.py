from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.utils import timezone
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from .forms import StudentRegistrationForm
# import threading 

from .models import (
    ManagementTeam, Course, News, Category,
    GalleryImage, DonationDetails, ContactMessage, Testimonial, StudentRegistration, AlumniProfile,AlumniEvent
)

from .forms import (
    CategoryForm,
    GalleryImageForm,
    DonationForm,
)

# ==================== AUTHENTICATION VIEWS ====================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_panel:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('admin_panel:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'authenticate/login.html') 

@login_required(login_url='admin_panel:login')
def logout_view(request):
    logout(request)
    return redirect('admin_panel:login')


# ==================== DASHBOARD OVERVIEW ====================

@login_required(login_url='admin_panel:login')
def dashboard(request):
    context = {
        'total_team': ManagementTeam.objects.count(),
        'total_courses': Course.objects.count(),
        'total_news': News.objects.count(),
        'total_albums': GalleryImage.objects.count(),
        'total_donations': DonationDetails.objects.count(),
        'total_messages': ContactMessage.objects.all().count(),
        # 'total_downloads': Download.objects.count(),
        'total_testimonials': Testimonial.objects.count(),
        'recent_messages': ContactMessage.objects.all().order_by('-created_at')[:5],
        'recent_donations': DonationDetails.objects.all().order_by('-donated_at')[:5],
    }
    return render(request, 'admin_panel/dashboard.html', context)


# ==================== MANAGEMENT TEAM VIEWS ====================
@login_required(login_url='admin_panel:login')
def team_list(request):
    team_list = ManagementTeam.objects.all().order_by('name')
    paginator = Paginator(team_list, 6)
    page = request.GET.get('page')
    
    try:
        team = paginator.page(page)
    except PageNotAnInteger:
        team = paginator.page(1)
    except EmptyPage:
        team = paginator.page(paginator.num_pages)
    
    return render(request, 'admin_panel/team_list.html', {'team': team})

@login_required(login_url='admin_panel:login')
def team_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        photo = request.FILES.get('photo')
        
        ManagementTeam.objects.create(
            name=name,
            position=position,
            photo=photo
        )
        messages.success(request, 'Team member added successfully!')
        return redirect('admin_panel:team_list')
    
    return render(request, 'admin_panel/team_form.html')

@login_required(login_url='admin_panel:login')
def team_edit(request, pk):
    team = get_object_or_404(ManagementTeam, pk=pk)
    
    if request.method == 'POST':
        team.name = request.POST.get('name')
        team.position = request.POST.get('position')
        
        if request.FILES.get('photo'):
            team.photo = request.FILES.get('photo')
        
        team.save()
        messages.success(request, 'Team member updated successfully!')
        return redirect('admin_panel:team_list')
    
    return render(request, 'admin_panel/team_form.html', {'team': team})

@login_required(login_url='admin_panel:login')
def team_delete(request, pk):
    team = get_object_or_404(ManagementTeam, pk=pk)
    team.delete()
    messages.success(request, 'Team member deleted successfully!')
    return redirect('admin_panel:team_list')


# ==================== COURSE VIEWS ====================
@login_required(login_url='admin_panel:login')
def course_list(request):
    course_list = Course.objects.all().order_by('-created_at')
    paginator = Paginator(course_list, 6)
    page = request.GET.get('page')
    
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    
    return render(request, 'admin_panel/course_list.html', {'courses': courses})

@login_required(login_url='admin_panel:login')
def course_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        thumbnail = request.FILES.get('thumbnail')

        Course.objects.create(
            title=title,
            description=description,
            duration=duration,
            thumbnail=thumbnail
        )
        messages.success(request, 'Course added successfully!')
        return redirect('admin_panel:course_list')
    
    return render(request, 'admin_panel/course_form.html')


@login_required(login_url='admin_panel:login')
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.description = request.POST.get('description')
        course.duration = request.POST.get('duration')
        
        if request.FILES.get('thumbnail'):
            course.thumbnail = request.FILES.get('thumbnail')
        
        course.save()
        messages.success(request, 'Course updated successfully!')
        return redirect('admin_panel:course_list')
    
    return render(request, 'admin_panel/course_form.html', {'course': course})


@login_required(login_url='admin_panel:login')
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    messages.success(request, 'Course deleted successfully!')
    return redirect('admin_panel:course_list')


# ==================== NEWS VIEWS ====================
@login_required(login_url='admin_panel:login')
def news_list(request):
    news_list = News.objects.all().order_by('-published_date')
    paginator = Paginator(news_list, 6)
    page = request.GET.get('page')
    
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    
    return render(request, 'admin_panel/news_list.html', {'news': news})

@login_required(login_url='admin_panel:login')
def news_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        original_slug = slugify(title)
        slug = original_slug
        counter = 1
        while News.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        News.objects.create(
            title=title,
            slug=slug,
            content=content,
            image=image
        )
        messages.success(request, 'News added successfully!')
        return redirect('admin_panel:news_list')
    
    return render(request, 'admin_panel/news_form.html')

@login_required(login_url='admin_panel:login')
def news_edit(request, pk):
    news = get_object_or_404(News, pk=pk)
    
    if request.method == 'POST':
        new_title = request.POST.get('title')
        news.content = request.POST.get('content')
        
        if news.title != new_title:
            news.title = new_title
            original_slug = slugify(new_title)
            slug = original_slug
            counter = 1
            while News.objects.filter(slug=slug).exclude(pk=pk).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            news.slug = slug

        if request.FILES.get('image'):
            news.image = request.FILES.get('image')
        
        news.save()
        messages.success(request, 'News updated successfully!')
        return redirect('admin_panel:news_list')
    
    return render(request, 'admin_panel/news_form.html', {'news': news})

@login_required(login_url='admin_panel:login')
def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.delete()
    messages.success(request, 'News deleted successfully!')
    return redirect('admin_panel:news_list')


# ==================== GALLERY & CATEGORY VIEWS ====================

@login_required(login_url="admin_panel:login")
def gallery_images(request):
    categories = Category.objects.all().prefetch_related("images")
    category_pages = {}
    for category in categories:
        images_qs = category.images.all().order_by("-uploaded_at")
        paginator = Paginator(images_qs, 8)
        page_number = request.GET.get(f"page_{category.id}", 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        category_pages[category.id] = page_obj

    return render(
        request,
        "admin_panel/image_list.html",
        {
            "categories": categories,
            "category_pages": category_pages,
        },
    )

@login_required(login_url="admin_panel:login")
def add_image(request):
    categories = Category.objects.all()
    if request.method == "POST":
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        files = request.FILES.getlist("images")
        for file in files:
            GalleryImage.objects.create(
                category=category,
                title=file.name,
                image=file,
            )
        messages.success(request, "Images uploaded succesfully")
        return redirect("admin_panel:list_image")
    return render(request, "admin_panel/add_image.html", {"categories": categories})

@login_required(login_url="admin_panel:login")
def category_list(request):
    categories = Category.objects.all().order_by("-created_at")
    paginator = Paginator(categories, 10)
    page_number = request.GET.get("page")
    categories = paginator.get_page(page_number)
    return render(request, "admin_panel/category_list.html", {"categories": categories})

@login_required(login_url="admin_panel:login")
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name)
            return redirect("admin_panel:category_list")
    return render(request, "admin_panel/add_category.html")

@login_required(login_url="admin_panel:login")
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        return redirect("admin_panel:category_list")
    return redirect("admin_panel:category_list")

@login_required(login_url="admin_panel:login")
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("admin_panel:category_list")
    return redirect("admin_panel:category_list")

@login_required(login_url="admin_panel:login")
def delete_image(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)
    if request.method == "POST":
        image.delete()
        messages.success(request, "Image deleted successfully")
        return redirect("admin_panel:list_image")
    return render(request, "admin_panel/image_list.html", {"image": image})


# ==================== DONATION VIEWS ====================
@login_required(login_url='admin_panel:login')
def donation_list(request):
    donation_list = DonationDetails.objects.all().order_by('-donated_at')
    paginator = Paginator(donation_list, 6)
    page = request.GET.get('page')
    try:
        donations = paginator.page(page)
    except PageNotAnInteger:
        donations = paginator.page(1)
    except EmptyPage:
        donations = paginator.page(paginator.num_pages)
    return render(request, 'admin_panel/donation_list.html', {'donations': donations})

@login_required(login_url='admin_panel:login')
def donation_create(request):
    if request.method == 'POST':
        donor_name = request.POST.get('donor_name')
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        DonationDetails.objects.create(
            donor_name=donor_name,
            payment_method=payment_method,
            transaction_id=transaction_id,
            email=email,
            phone=phone,
            message=message
        )
        messages.success(request, 'Donation record added successfully!')
        return redirect('admin_panel:donation_list')
    return render(request, 'admin_panel/donation_form.html')

@login_required(login_url='admin_panel:login')
def donation_edit(request, pk):
    donation = get_object_or_404(DonationDetails, pk=pk)
    if request.method == 'POST':
        donation.donor_name = request.POST.get('donor_name')
        donation.payment_method = request.POST.get('payment_method')
        donation.transaction_id = request.POST.get('transaction_id')
        donation.email = request.POST.get('email')
        donation.phone = request.POST.get('phone')
        donation.message = request.POST.get('message')
        donation.save()
        messages.success(request, 'Donation record updated successfully!')
        return redirect('admin_panel:donation_list')
    return render(request, 'admin_panel/donation_form.html', {'donation': donation})

@login_required(login_url='admin_panel:login')
def donation_delete(request, pk):
    donation = get_object_or_404(DonationDetails, pk=pk)
    donation.delete()
    messages.success(request, 'Donation record deleted successfully!')
    return redirect('admin_panel:donation_list')

# ==================== CONTACT MESSAGE VIEWS ====================
@login_required(login_url='admin_panel:login')
def message_list(request):
    message_list = ContactMessage.objects.all().order_by('-created_at')
    paginator = Paginator(message_list, 6)
    page = request.GET.get('page')
    try:
        messages_list = paginator.page(page)
    except PageNotAnInteger:
        messages_list = paginator.page(1)
    except EmptyPage:
        messages_list = paginator.page(paginator.num_pages)
    return render(request, 'admin_panel/message_list.html', {'messages_list': messages_list})

@login_required(login_url='admin_panel:login')
def message_view(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    message.save()
    return render(request, 'admin_panel/message_view.html', {'message': message})

@login_required(login_url='admin_panel:login')
def message_delete(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    message.delete()
    messages.success(request, 'Message deleted successfully!')
    return redirect('admin_panel:message_list')


# # ==================== DOWNLOAD VIEWS ====================
# @login_required(login_url='admin_panel:login')
# def download_list(request):
#     download_list = Download.objects.all().order_by('-uploaded_at')
#     paginator = Paginator(download_list, 6)
#     page = request.GET.get('page')
#     try:
#         downloads = paginator.page(page)
#     except PageNotAnInteger:
#         downloads = paginator.page(1)
#     except EmptyPage:
#         downloads = paginator.page(paginator.num_pages)
#     return render(request, 'admin_panel/download_list.html', {'downloads': downloads})

# @login_required(login_url='admin_panel:login')
# def download_create(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         category = request.POST.get('category')
#         file = request.FILES.get('file')
#         file_size = request.POST.get('file_size')
#         Download.objects.create(
#             title=title,
#             description=description,
#             category=category,
#             file=file,
#             file_size=file_size
#         )
#         messages.success(request, 'Download added successfully!')
#         return redirect('admin_panel:download_list')
#     return render(request, 'admin_panel/download_form.html')

# @login_required(login_url='admin_panel:login')
# def download_edit(request, pk):
#     download = get_object_or_404(Download, pk=pk)
#     if request.method == 'POST':
#         download.title = request.POST.get('title')
#         download.description = request.POST.get('description')
#         download.category = request.POST.get('category')
#         download.file_size = request.POST.get('file_size')
#         if request.FILES.get('file'):
#             download.file = request.FILES.get('file')
#         download.save()
#         messages.success(request, 'Download updated successfully!')
#         return redirect('admin_panel:download_list')
#     return render(request, 'admin_panel/download_form.html', {'download': download})

# @login_required(login_url='admin_panel:login')
# def download_delete(request, pk):
#     download = get_object_or_404(Download, pk=pk)
#     download.delete()
#     messages.success(request, 'Download deleted successfully!')
#     return redirect('admin_panel:download_list')


# ==================== TESTIMONIAL VIEWS ====================
@login_required(login_url='admin_panel:login')
def testimonial_list(request):
    testimonial_list = Testimonial.objects.all().order_by('-created_at')
    paginator = Paginator(testimonial_list, 6)
    page = request.GET.get('page')
    try:
        testimonials = paginator.page(page)
    except PageNotAnInteger:
        testimonials = paginator.page(1)
    except EmptyPage:
        testimonials = paginator.page(paginator.num_pages)
    return render(request, 'admin_panel/testimonial_list.html', {'testimonials': testimonials})

@login_required(login_url='admin_panel:login')
def testimonial_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        content = request.POST.get('content')
        rating = request.POST.get('rating', 5)
        photo = request.FILES.get('photo')
        Testimonial.objects.create(
            name=name,
            designation=designation,
            content=content,
            rating=rating,
            photo=photo
        )
        messages.success(request, 'Testimonial added successfully!')
        return redirect('admin_panel:testimonial_list')
    return render(request, 'admin_panel/testimonial_form.html')

@login_required(login_url='admin_panel:login')
def testimonial_edit(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.name = request.POST.get('name')
        testimonial.designation = request.POST.get('designation')
        testimonial.content = request.POST.get('content')
        testimonial.rating = request.POST.get('rating', 5)
        if request.FILES.get('photo'):
            testimonial.photo = request.FILES.get('photo')
        testimonial.save()
        messages.success(request, 'Testimonial updated successfully!')
        return redirect('admin_panel:testimonial_list')
    return render(request, 'admin_panel/testimonial_form.html', {'testimonial': testimonial})

@login_required(login_url='admin_panel:login')
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, 'Testimonial deleted successfully!')
    return redirect('admin_panel:testimonial_list')


# ==================== PUBLIC WEBSITE VIEWS (Frontend) ====================
def index(request):
    courses = Course.objects.filter(is_active=True).order_by('-created_at')[:4]
    news = News.objects.filter(is_published=True).order_by('-published_date')[:3]
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')
    gallery_images = GalleryImage.objects.all().order_by('-uploaded_at')[:8]
    total_courses = Course.objects.filter(is_active=True).count()
    total_team = ManagementTeam.objects.count()
    context = {
        'courses': courses,
        'news': news,
        'testimonials': testimonials,
        'gallery_images': gallery_images,
        'total_courses': total_courses,
        'total_team': total_team,
    }
    return render(request, 'index.html', context)


def about_page(request):
    team = ManagementTeam.objects.all().order_by('name')
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')
    context = {
        'team': team,
        'testimonials': testimonials,
    }
    return render(request, 'about.html', context)

def our_team(request):
    team_qs = ManagementTeam.objects.all().order_by('name')
    paginator = Paginator(team_qs, 6) 
    page_number = request.GET.get('page')
    team = paginator.get_page(page_number)
    return render(request, 'team.html', {'team': team})

def courses_page(request):
    course_list = Course.objects.filter(is_active=True).order_by('-created_at')
    paginator = Paginator(course_list, 8) 
    page_number = request.GET.get('page')
    try:
        courses = paginator.page(page_number)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    context = {'courses': courses}
    return render(request, 'courses.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    all_courses = Course.objects.filter(is_active=True).exclude(slug=slug).order_by('-created_at')
    context = {
        'course': course,
        'all_courses': all_courses,
    }
    return render(request, 'course-detail.html', context)

def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('username') or request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject, 
            message=message
        )
        return render(request, 'contact.html', {'success': True})
    return render(request, 'contact.html')

def blog_page(request):
    search_query = request.GET.get('search-field') or request.POST.get('search-field')
    news_list = News.objects.filter(is_published=True).order_by('-published_date')
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    paginator = Paginator(news_list, 6)
    page_number = request.GET.get('page')
    try:
        news = paginator.page(page_number)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    context = {
        'news': news,
        'search_query': search_query
    }
    return render(request, 'blog.html', context)

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    recent_news = News.objects.filter(is_published=True).exclude(slug=slug).order_by('-published_date')[:3]
    categories = Category.objects.all()
    context = {
        'news': news,
        'recent_news': recent_news,
        'categories': categories,
    }
    return render(request, 'news-detail.html', context)

def services_page(request):
    return render(request, 'services.html')

def service_detail(request, pk):
    return render(request, 'service-detail.html')

def prayer_time(request):
    return render(request, 'prayer-time.html')

def faq_page(request):
    return render(request, 'faq.html')

def not_found_page(request):
    return render(request, 'not-found.html')

def gallery_page(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    images_list = GalleryImage.objects.all().order_by('-uploaded_at')
    if category_id:
        images_list = images_list.filter(category__id=category_id)
    paginator = Paginator(images_list, 9)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    context = {
        'images': images,
        'categories': categories,
        'active_category': int(category_id) if category_id else None
    }
    return render(request, 'gallery.html', context)

#public donate view
def donate(request):
    if request.method == 'POST':
        donor_name = request.POST.get('donor_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        screenshot = request.FILES.get('screenshot') 

        DonationDetails.objects.create(
            donor_name=donor_name,
            email=email,
            phone=phone,
            screenshot=screenshot,
        )
        messages.success(request, "Thank you! Your donation details have been submitted for verification.")
        return redirect('admin_panel:donate')
    
    return render(request, 'donate.html')


# ==================== PUBLIC REGISTRATION VIEW ====================

# def send_email_in_thread(subject, message, recipient_list):
#     try:
#         print("Attempting to send email...") 
#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             recipient_list,
#             fail_silently=False,
#         )
#         print("Email sent successfully!") 
#     except Exception as e:
#         print(f"Error sending email: {e}")

# def register_view(request):
#     form = StudentRegistrationForm()
    
#     if request.method == 'POST':
#         form = StudentRegistrationForm(request.POST)
        
#         if form.is_valid():
#             student = form.save()
            
#             course_title = student.course.title if student.course else "Not Selected"
#             program_specific = student.program_name if student.program_name else "N/A"
            
#             subject = f"New Student Registration: {student.first_name} {student.last_name}"
            
#             message = (
#                 f"A new student has registered via the website.\n\n"
#                 f"--------------------------------------------\n"
#                 f"FULL NAME: {student.first_name} {student.last_name}\n"
#                 f"DOB:       {student.dob}\n"
#                 f"EMAIL:     {student.email}\n"
#                 f"MOBILE:    {student.mobile}\n"
#                 f"--------------------------------------------\n"
#                 f"COURSE:     {course_title}\n"
#                 f"SPECIFIC PROGRAM: {program_specific}\n"
#                 f"--------------------------------------------\n\n"
#                 f"Please verify this entry in the Admin Panel."
#             )
            
#             recipient_list = [settings.EMAIL_HOST_USER]  
            
#             email_thread = threading.Thread(
#                 target=send_email_in_thread, 
#                 args=(subject, message, recipient_list)
#             )
#             email_thread.start()

#             messages.success(request, 'Registration successful! We have received your details.')
#             return redirect('admin_panel:register')
            
#         else:
#             messages.error(request, 'Please correct the errors in the form below.')
            
#     return render(request, 'register.html', {'form': form})



def register_view(request):
    form = StudentRegistrationForm()

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            student = form.save()

            course_title = student.course.title if student.course else "Not Selected"
            program_specific = student.program_name if student.program_name else "N/A"

            subject = f"New Student Registration: {student.first_name} {student.last_name}"

            message = (
                f"A new student has registered via the website.\n\n"
                f"--------------------------------------------\n"
                f"FULL NAME: {student.first_name} {student.last_name}\n"
                f"DOB:       {student.dob}\n"
                f"EMAIL:     {student.email}\n"
                f"MOBILE:    {student.mobile}\n"
                f"--------------------------------------------\n"
                f"COURSE:     {course_title}\n"
                f"SPECIFIC PROGRAM: {program_specific}\n"
                f"--------------------------------------------\n\n"
                f"Please verify this entry in the Admin Panel."
            )

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                print("Email error:", e)

            messages.success(
                request,
                "Registration successful! We have received your details."
            )
            return redirect('admin_panel:register')

        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'register.html', {'form': form})


# # ==================== STUDENT REGISTRATION VIEWS FOR LOCAL HOSTING ====================
# def register_view(request):
#     form = StudentRegistrationForm()

#     if request.method == 'POST':
#         form = StudentRegistrationForm(request.POST)

#         if form.is_valid():
#             student = form.save()

#             course_title = student.course.title if student.course else "Not Selected"
#             program_specific = student.program_name if student.program_name else "N/A"

#             subject = f"New Student Registration: {student.first_name} {student.last_name}"

#             message = (
#                 f"A new student has registered via the website.\n\n"
#                 f"FULL NAME: {student.first_name} {student.last_name}\n"
#                 f"DOB:       {student.dob}\n"
#                 f"EMAIL:     {student.email}\n"
#                 f"MOBILE:    {student.mobile}\n"
#                 f"COURSE:     {course_title}\n"
#                 f"SPECIFIC PROGRAM: {program_specific}\n"
#             )

#             try:
#                 send_mail(
#                     subject,
#                     message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     [settings.EMAIL_HOST_USER],
#                     fail_silently=False,  
#                 )
#                 print("Email sent successfully")
#             except Exception as e:
#                 print("Email failed locally:", e)

#             messages.success(
#                 request,
#                 "Registration successful! We have received your details."
#             )
#             return redirect('admin_panel:register')

#         else:
#             messages.error(request, "Please correct the errors below.")

#     return render(request, 'register.html', {'form': form})



# ==================== STUDENT REGISTRATION VIEWS (admin dashboard)====================
@login_required(login_url='admin_panel:login')
def student_list(request):
    student_list = StudentRegistration.objects.all().order_by('-registered_at')
    paginator = Paginator(student_list, 10) 
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    return render(request, 'admin_panel/student_list.html', {'students': students})


@login_required(login_url='admin_panel:login')
def student_delete(request, pk):
    student = get_object_or_404(StudentRegistration, pk=pk)
    student.delete()
    messages.success(request, 'Student registration removed successfully.')
    return redirect('admin_panel:student_list')


def page404(request, exception):
    return render(request, 'not-found.html', status=404)




# ==================== ALUMNI PROFILE VIEWS ====================

@login_required(login_url='admin_panel:login')
def alumni_list(request):
    """Lists all alumni with pagination in the custom admin dashboard."""
    alumni_qs = AlumniProfile.objects.all().order_by('-created_at')
    paginator = Paginator(alumni_qs, 10) 
    page = request.GET.get('page')
    
    try:
        alumni_list = paginator.page(page)
    except PageNotAnInteger:
        alumni_list = paginator.page(1)
    except EmptyPage:
        alumni_list = paginator.page(paginator.num_pages)
        
    return render(request, 'admin_panel/alumni_list.html', {'alumni_list': alumni_list})


@login_required(login_url='admin_panel:login')
def alumni_create(request):
    """Handles the creation of a new alumni profile."""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        photo = request.FILES.get('photo')
        
        AlumniProfile.objects.create(
            name=name,
            description=description,
            photo=photo
        )
        
        messages.success(request, 'Alumni profile created successfully!')
        return redirect('admin_panel:alumni_list')
    
    return render(request, 'admin_panel/alumni_form.html')


@login_required(login_url='admin_panel:login')
def alumni_edit(request, pk):
    """Handles editing an existing alumni profile."""
    alumni = get_object_or_404(AlumniProfile, pk=pk)
    
    if request.method == 'POST':
        alumni.name = request.POST.get('name')
        alumni.description = request.POST.get('description')
        
        if request.FILES.get('photo'):
            alumni.photo = request.FILES.get('photo')
            
        alumni.save()
        messages.success(request, 'Alumni profile updated successfully!')
        return redirect('admin_panel:alumni_list')
    
    return render(request, 'admin_panel/alumni_form.html', {'alumni': alumni})


@login_required(login_url='admin_panel:login')
def alumni_delete(request, pk):
    """Handles deletion of an alumni profile."""
    alumni = get_object_or_404(AlumniProfile, pk=pk)
    alumni.delete()
    messages.success(request, 'Alumni profile deleted successfully!')
    return redirect('admin_panel:alumni_list')



# ==================== ALUMNI EVENT VIEWS ====================
@login_required(login_url='admin_panel:login')
def alumni_event_list(request):
    event_list = AlumniEvent.objects.all().order_by('-date')
    paginator = Paginator(event_list, 6)  
    page = request.GET.get('page')
    
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    
    return render(request, 'admin_panel/alumni_event_list.html', {'events': events})

@login_required(login_url='admin_panel:login')
def alumni_event_create(request):
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        date = request.POST.get('date')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        AlumniEvent.objects.create(
            event_name=event_name,
            date=date,
            description=description,
            image=image, 
            is_visible='is_visible' in request.POST  
        )
        messages.success(request, 'Alumni Event added successfully!')
        return redirect('admin_panel:alumni_event_list')
    
    return render(request, 'admin_panel/alumni_event_form.html')

@login_required(login_url='admin_panel:login')
def alumni_event_edit(request, pk):
    event = get_object_or_404(AlumniEvent, pk=pk)
    
    if request.method == 'POST':
        event.event_name = request.POST.get('event_name')
        event.date = request.POST.get('date')
        event.description = request.POST.get('description')
        
        if request.FILES.get('image'):
            event.image = request.FILES.get('image')
        
        event.is_visible = 'is_visible' in request.POST 
        
        event.save()
        messages.success(request, 'Alumni Event updated successfully!')
        return redirect('admin_panel:alumni_event_list')
    
    return render(request, 'admin_panel/alumni_event_list.html', {'event': event})

@login_required(login_url='admin_panel:login')
def alumni_event_delete(request, pk):
    event = get_object_or_404(AlumniEvent, pk=pk)
    event.delete()
    messages.success(request, 'Alumni Event deleted successfully!')
    return redirect('admin_panel:alumni_event_list')

def alumni_public_view(request):
    events = AlumniEvent.objects.filter(is_visible=True).order_by('-date')
    alumni_list = AlumniProfile.objects.all().order_by('-created_at')
    paginator = Paginator(alumni_list, 6) 
    page = request.GET.get('page')
    try:
        alumni = paginator.page(page)
    except PageNotAnInteger:
        alumni = paginator.page(1)
    except EmptyPage:
        alumni = paginator.page(paginator.num_pages)

    context = {
        'events': events,
        'alumni': alumni,
    }
    return render(request, 'alumni.html', context)





# ==================== email message in html format ====================

# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags

# def register_view(request):
#     form = StudentRegistrationForm()

#     if request.method == 'POST':
#         form = StudentRegistrationForm(request.POST)

#         if form.is_valid():
#             student = form.save()

#             course_title = student.course.title if student.course else "Not Selected"
#             program_specific = student.program_name if student.program_name else "N/A"

#             subject = f"New Registration: {student.first_name} {student.last_name}"

#             # HTML Email Content
#             html_message = f"""
#             <!DOCTYPE html>
#             <html>
#             <head>
#                 <meta charset="UTF-8">
#             </head>
#             <body style="margin:0; padding:0; background-color:#f4f4f4; font-family: Arial, sans-serif;">
#                 <table width="100%" cellpadding="0" cellspacing="0" style="padding: 40px 20px;">
#                     <tr>
#                         <td align="center">
#                             <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:8px; overflow:hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                
#                                 <!-- Header -->
#                                 <tr>
#                                     <td style="background: #2D4636; padding: 30px; text-align: center;">
#                                         <h1 style="margin:0; color:#ffffff; font-size:22px; font-weight:600;">
#                                             New Student Registration
#                                         </h1>
#                                     </td>
#                                 </tr>
                                
#                                 <!-- Body -->
#                                 <tr>
#                                     <td style="padding: 35px 40px;">
#                                         <p style="margin:0 0 25px; color:#555; font-size:15px; line-height:1.6;">
#                                             A new student has registered on the website. Here are the details:
#                                         </p>
                                        
#                                         <!-- Data Table -->
#                                         <table width="100%" cellpadding="0" cellspacing="0" style="border: 1px solid #e0e0e0; border-radius: 6px; overflow: hidden;">
#                                             <tr style="background: #f8f9fa;">
#                                                 <td style="padding: 14px 20px; font-weight: 600; color: #2D4636; border-bottom: 1px solid #e0e0e0; width: 40%;">Full Name</td>
#                                                 <td style="padding: 14px 20px; color: #333; border-bottom: 1px solid #e0e0e0;">{student.first_name} {student.last_name}</td>
#                                             </tr>
#                                             <tr>
#                                                 <td style="padding: 14px 20px; font-weight: 600; color: #2D4636; border-bottom: 1px solid #e0e0e0;">Date of Birth</td>
#                                                 <td style="padding: 14px 20px; color: #333; border-bottom: 1px solid #e0e0e0;">{student.dob}</td>
#                                             </tr>
#                                             <tr style="background: #f8f9fa;">
#                                                 <td style="padding: 14px 20px; font-weight: 600; color: #2D4636; border-bottom: 1px solid #e0e0e0;">Email</td>
#                                                 <td style="padding: 14px 20px; color: #333; border-bottom: 1px solid #e0e0e0;">{student.email}</td>
#                                             </tr>
#                                             <tr>
#                                                 <td style="padding: 14px 20px; font-weight: 600; color: #2D4636; border-bottom: 1px solid #e0e0e0;">Mobile</td>
#                                                 <td style="padding: 14px 20px; color: #333; border-bottom: 1px solid #e0e0e0;">{student.mobile}</td>
#                                             </tr>
#                                             <tr style="background: #f8f9fa;">
#                                                 <td style="padding: 14px 20px; font-weight: 600; color: #2D4636; border-bottom: 1px solid #e0e0e0;">Course</td>
#                                                 <td style="padding: 14px 20px; color: #333; border-bottom: 1px solid #e0e0e0;">{course_title}</td>
#                                             </tr>
#                                             <tr>
#                                                 <td style="padding: 14px 20px; font-weight: 600; color: #2D4636;">Program</td>
#                                                 <td style="padding: 14px 20px; color: #333;">{program_specific}</td>
#                                             </tr>
#                                         </table>
#                                     </td>
#                                 </tr>
                                
#                                 <!-- Footer -->
#                                 <tr>
#                                     <td style="background: #f8f9fa; padding: 20px 40px; text-align: center; border-top: 1px solid #e0e0e0;">
#                                         <p style="margin:0; color:#888; font-size:13px;">
#                                             Darul Fatheh Islamic Complex
#                                         </p>
#                                     </td>
#                                 </tr>
                                
#                             </table>
#                         </td>
#                     </tr>
#                 </table>
#             </body>
#             </html>
#             """

#             plain_message = strip_tags(html_message)

#             try:
#                 email = EmailMultiAlternatives(
#                     subject,
#                     plain_message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     [settings.EMAIL_HOST_USER],
#                 )
#                 email.attach_alternative(html_message, "text/html")
#                 email.send(fail_silently=False)
#                 print("Email sent successfully")
#             except Exception as e:
#                 print("Email failed:", e)

#             messages.success(
#                 request,
#                 "Registration successful! We have received your details."
#             )
#             return redirect('admin_panel:register')

#         else:
#             messages.error(request, "Please correct the errors below.")

#     return render(request, 'register.html', {'form': form})
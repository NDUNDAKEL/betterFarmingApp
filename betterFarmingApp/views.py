
from django.conf import settings
from django.core.paginator import Paginator
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Plant, PlantImage,CustomUser, Testimonial
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.utils.timezone import now
from django.http import HttpResponse

from googleapiclient.errors import HttpError
from betterFarmingApp import models

# Create your views here.

def edit_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        # Update plant fields
        plant.name = request.POST['plant_name']
        plant.region = request.POST['region']
        plant.rainfall = request.POST['rainfall']
        plant.description = request.POST['description']
        plant.save()

        # Handle image deletions
        images_to_delete = request.POST.getlist('delete_images')
        if images_to_delete:
            PlantImage.objects.filter(id__in=images_to_delete).delete()

        # Handle new image uploads
        if 'plant_images' in request.FILES:
            images = request.FILES.getlist('plant_images')
            for image in images:
                PlantImage.objects.create(plant=plant, image=image)

        return redirect('plant_list')  # Redirect to the plant list or detail view

    return render(request, 'edit_plant.html', {'plant': plant})

def delete_plant(request, plant_id):
    # Retrieve the plant object by ID and delete it
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    return redirect('plant_list')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        region = request.POST.get('region')
        rainfall = request.POST.get('rainfall')
        profile_picture = request.FILES.get('profile_picture')  # Handle the uploaded file

        # Validate input
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')

        # Log the profile picture to see if it's being uploaded correctly
        if profile_picture:
            print(f"Profile picture uploaded: {profile_picture.name}")
        else:
            print("No profile picture uploaded.")

        # Create user using Django's create_user method
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            region=region,
            rainfall=rainfall,
            profile_picture=profile_picture  # Save the profile picture
        )

        # Log in the user after successful signup
       
        messages.success(request, "Sign-up successful!")
        return redirect('loginPage')

    return render(request, 'signup.html')
def loginFunction(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  
            messages.success(request, "Login successful!")
            return redirect('home')
                
           

        else:
            messages.error(request, "Invalid credentials!")
            return redirect('loginPage')

    return render(request, 'loginPage.html')
def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('home')

def home(request):
    context = {
        'user': request.user
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def plant_list(request):
    # Fetch all plants along with their images
    plants = Plant.objects.prefetch_related('images').all()
    if request.user.is_authenticated and request.user.username !='admin':
        # Assuming the user has a `region` attribute
        user_region = request.user.region
        user_plants = Plant.objects.filter(region__icontains=user_region)
    else:
        user_plants = Plant.objects.none()  # No plants if the user is not authenticated


    context = {
        'plants': plants,
        'user_plants': user_plants,
    }
    return render(request, 'plant_list.html', context)

def contact(request):
    return render(request, 'contact.html')

def services(request):
        reviewToEdit = None  # Initialize outside the conditions to avoid scope issues
        edited=None
        if request.method == "POST":
            # Check if user submitted an edit form
        
            if 'editPost' in request.POST:
                review_id = request.POST.get('editPost')
                try:
                    # Fetch the review to edit
                    reviewToEdit = Testimonial.objects.get(id=review_id)
                    if request.user.is_authenticated and reviewToEdit.reviewerid == request.user.id :
                        # Update review with new content
                        new_content = request.POST.get('content', '').strip()
                        if reviewToEdit:
                            if new_content:
                                reviewToEdit.content = new_content
                                reviewToEdit.date_sent = now()
                                reviewToEdit.save()
                                messages.success(request, "Review edited successfully.")
                                edited=True
                                return redirect('services')  # Redirect to prevent resubmission
                            else:
                                messages.error(request, "Content cannot be empty.")
                    else:
                        messages.error(request, "You are not authorized to edit this review.")
                except Testimonial.DoesNotExist:
                    messages.error(request, "The review does not exist.")

            # Check if user submitted a delete form
            elif 'deleteReview' in request.POST:
                review_id = request.POST.get('deleteReview')
                try:
                    review = Testimonial.objects.get(id=review_id)
                    if request.user.is_authenticated and review.reviewerid == request.user.id:
                        review.delete()
                        messages.success(request, "Review deleted successfully.")
                    else:
                        messages.error(request, "You are not authorized to delete this review.")
                except Testimonial.DoesNotExist:
                    messages.error(request, "The review does not exist.")

            # Check if user is adding a new review
            else:
                content = request.POST.get("content", "").strip()
                if not content:
                    messages.error(request, "Testimonial content cannot be empty!")
                else:
                
                    # Add a new testimonial
                        Profile_image = request.user.profile_picture
                        reviewer = request.user.username
                        userid = request.user.id
                        Testimonial.objects.create(
                            content=content, 
                            profile_image=Profile_image, 
                            reviewer=reviewer, 
                            reviewerid=userid
                        )
                        messages.success(request, "Your testimonial was successfully submitted.")
                        return redirect('services')  # Redirect to prevent resubmission

        # Fetch and paginate reviews
        reviews = Testimonial.objects.all().order_by('-date_sent')
        paginator = Paginator(reviews, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'reviews': page_obj,
            'edited':edited,
            'reviewToEdit': reviewToEdit,  # Pass the review to edit to the template
        }
        return render(request, "services.html", context)

def testimonials(request):
    return render(request, 'testimonials.html')
def blog(request):
    return render(request, 'blog.html')
def login(request):
    return render(request, 'login.html')
def adminLogin(request):
    return render(request, 'adminLogin.html')
def signup(request):
    return render(request, 'signUp.html')


# Add Plant view
def add_plant(request):
    if request.method == 'POST':
        try:
            # Retrieve form data
            plant_name = request.POST.get('plant_name')
            region = request.POST.get('region')
            rainfall = request.POST.get('rainfall')
            description = request.POST.get('description')

            # Validate form data
            if not plant_name or not region or not rainfall or not description:
                raise ValidationError("All fields are required.")

            # Create and save the Plant object
            plant = Plant.objects.create(
                name=plant_name,
                region=region,
                rainfall=rainfall,
                description=description
            )

            # Handle multiple image uploads
            images = request.FILES.getlist('plant_images')  # Expecting 'plant_images' as input field name
            if images:
                for image in images:
                    PlantImage.objects.create(plant=plant, image=image)

            # Add a success message
            messages.success(request, f'Plant "{plant_name}" has been successfully added!')
            return redirect('plant_list')  # Redirect to the plant list page after success
        except ValidationError as ve:
            messages.error(request, f"Validation error: {ve.message}")
        except Exception as e:
            messages.error(request, 'An error occurred while adding the plant. Please try again.')

        # If any errors, render the form again with the error messages
        return redirect('add_plant')  # or render with messages depending on your flow

    # Render the form for GET requests
    return render(request, 'addPlants.html')


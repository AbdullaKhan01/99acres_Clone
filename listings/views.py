from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Property



def home(request):
    latest_properties = Property.objects.all().order_by('-date_posted')[:4]
    return render(request, 'listings/home.html', {'properties': latest_properties})

def all_listings(request):
    all_properties = Property.objects.all().order_by('-date_posted')
    return render(request, 'listings/all_listings.html', {'properties': all_properties})

def property_detail(request, pk):
    property_item = get_object_or_404(Property, pk=pk)
    return render(request, 'listings/property_detail.html', {'property': property_item})


def search(request):
    query = request.GET.get('q', '').strip()           # city or location
    property_type = request.GET.get('type', 'ALL').strip()   # Apartment, Plot, etc.

    # start with all properties
    properties = Property.objects.all()

    # ✅ Filter by city/location/title/description if query exists
    if query:
        properties = properties.filter(
            Q(location__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    # ✅ Filter by property type if not ALL
    if property_type and property_type.upper() != 'ALL':
        properties = properties.filter(property_type__iexact=property_type)

    context = {
        'properties': properties,
        'query': query,
        'type': property_type
    }

    return render(request, 'listings/search.html', context)
@login_required(login_url='login')
def add_property(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        property_type = request.POST.get('property_type')
        price = request.POST.get('price')
        location = request.POST.get('location')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        area = request.POST.get('area')
        image = request.FILES.get('image')

        Property.objects.create(
            title=title,
            description=description,
            property_type=property_type,
            price=price,
            location=location,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area=area,
            image=image,
            created_by=request.user   # ✅ add this line
        )

        messages.success(request, 'Your property has been listed successfully!')
        return redirect('home')

    return render(request, 'listings/add_property.html')

@login_required
def edit_property(request, pk):
    property_item = get_object_or_404(Property, pk=pk)

    # Only the creator can edit the property
    if property_item.created_by != request.user:
        return HttpResponseForbidden("You are not allowed to edit this property.")

    if request.method == 'POST':
        property_item.title = request.POST.get('title')
        property_item.description = request.POST.get('description')
        property_item.property_type = request.POST.get('property_type')
        property_item.price = request.POST.get('price')
        property_item.location = request.POST.get('location')
        property_item.bedrooms = request.POST.get('bedrooms')
        property_item.bathrooms = request.POST.get('bathrooms')
        property_item.area = request.POST.get('area')
        if request.FILES.get('image'):
            property_item.image = request.FILES['image']
        property_item.save()
        return redirect('property_detail', pk=property_item.pk)

    return render(request, 'listings/edit_property.html', {'property': property_item})

@login_required
def my_listings(request):
    user_properties = Property.objects.filter(created_by=request.user).order_by('-date_posted')
    return render(request, 'listings/my_listings.html', {'properties': user_properties})


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'listings/register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # change 'home' to your homepage url name
        else:
            messages.error(request, '⚠️ Invalid username or password. Please try again.')
            # Explicitly return same page with 401 status (helps Chrome realize login failed)
            response = render(request, 'listings/login.html')
            response.status_code = 401
            return response
    return render(request, 'listings/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')
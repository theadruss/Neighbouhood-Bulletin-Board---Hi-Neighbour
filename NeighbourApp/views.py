from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from NeighbourApp.models import CustomUser , Post
from django.contrib.auth.decorators import login_required

User  = CustomUser 

@login_required
def local(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get("category", "General")
        image = request.FILES.get("image")

        if not title or not content:
            messages.error(request, "Title and content are required.")
            return redirect("local")

        try:
            post = Post.objects.create(
                user=request.user,
                title=title,
                content=content,
                category=category,
                image=image
            )
            messages.success(request, "Your post has been published!")
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")

        return redirect("local")

    sort_order = request.GET.get("sort", "latest")
    category_filter = request.GET.get("category")
    if category_filter:
        posts = Post.objects.filter(category=category_filter).order_by('category')  # Sort by category
    else:
        posts = Post.objects.all().order_by("-timestamp")

    return render(request, "local.html", {
        "posts": posts,
        "user": request.user  # Pass the user object to the template
    })

def group(request):
    return render(request, 'group.html')

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        state = request.POST.get('state')

        if CustomUser .objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
        else:
            try:
                user = CustomUser (username=username, email=email, state=state)
                user.set_password(password)  # Hashes password before saving
                user.save()

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Signup successful! Welcome, {username}.")
                    return redirect('local')
                else:
                    messages.error(request, "Authentication failed after signup.")
            except Exception as e:
                messages.error(request, f"Error creating user: {e}")
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('local')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'signup.html')
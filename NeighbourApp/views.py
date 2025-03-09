from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from NeighbourApp.models import CustomUser
from NeighbourApp.models import Post
from django.contrib.auth.decorators import login_required

User = CustomUser

@login_required
def local(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get("category", "General")
        image = request.FILES.get("image")

        # Debugging: Check if data is received
        print("🔹 Received POST Data:", request.POST)
        print("🔹 Received FILES Data:", request.FILES)

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
            print("✅ Post Created:", post)
            messages.success(request, "Your post has been published!")
        except Exception as e:
            print("❌ Error creating post:", e)
            messages.error(request, "Something went wrong. Please try again.")

        return redirect("local")

    # Fetch posts with sorting
    sort_order = request.GET.get("sort", "latest")
    posts = Post.objects.all().order_by("-timestamp" if sort_order == "latest" else "timestamp")

    return render(request, "local.html", {"posts": posts})

def group(request):
    return render (request, 'group.html')

def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')  # Distinguish between signup & login

        if form_type == 'signup':
            # ✅ Handle Signup
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            state = request.POST.get('state')

            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose another.")
            else:
                try:
                    # ✅ Create user with hashed password
                    user = CustomUser(username=username, email=email, state=state)
                    user.set_password(password)  # Hashes password before saving
                    user.save()

                    # ✅ Authenticate and log in the user
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, f"Signup successful! Welcome, {username}.")
                        return redirect('local')  # Redirect to local news page
                    else:
                        messages.error(request, "Authentication failed after signup.")
                except Exception as e:
                    messages.error(request, f"Error creating user: {e}")
    return render(request, 'signup.html')  # Render signup page if GET request

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/localnews/')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'signup.html')



def local(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get("category", "General")
        image = request.FILES.get("image")

        if title and content:
            Post.objects.create(
                user=request.user,
                title=title,
                content=content,
                category=category,
                image=image
            )
            return redirect("local")  # Redirect to refresh the page after posting

    sort_order = request.GET.get("sort", "latest")
    posts = Post.objects.all().order_by("-timestamp" if sort_order == "latest" else "timestamp")

    return render(request, "local.html", {"posts": posts})

def group(request):
    return render (request, 'group.html')

def submit_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')

        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in to post.")
            return redirect('login')  # Redirect to login if user is not authenticated

        post = Post(title=title, content=content, category=category, user=request.user)  # ✅ Assign logged-in user
        post.save()

        messages.success(request, "Post created successfully!")
        return redirect('local')  # Redirect to local page after posting


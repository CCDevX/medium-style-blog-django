import os
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms.commentForm import CommentForm
from .forms.contactForm import ContactForm
from django.shortcuts import render, get_object_or_404, redirect

from .forms.postForm import PostForm
from .forms.profileForm import ProfileForm
from .models import Post, Profile
from .models import Comment


# Create your views here.

def index(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blog/index.html', {'posts': posts})


def post(request):
    posts_list = Post.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(posts_list, 9)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        print('Page is not an integer')
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except:
        posts = paginator.page(1)

    return render(request, 'blog/post.html', {'posts': posts})


def single_post(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            form.save()
            messages.success(request, 'Votre commentaire a été posté.')
            return redirect('blog-single-post', id=id)
    else:
        form = CommentForm()
    return render(request, 'blog/single-post.html', {'post': post, 'comments': comments, 'form': form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Merci pour votre message. Nous vous répondrons dans les plus brefs délais.')
            return redirect('blog-contact')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})


@login_required
def dashboard(request):
    published_posts_list = Post.objects.filter(is_published=True, author=request.user).order_by('-created_at')
    published_paginator = Paginator(published_posts_list, 9)
    published_page = request.GET.get('page', 1)

    try:
        published_posts = published_paginator.page(published_page)
    except PageNotAnInteger:
        published_posts = published_paginator.page(1)
    except EmptyPage:
        published_posts = published_paginator.page(published_paginator.num_pages)
    except:
        published_posts = published_paginator.page(1)

    draft_posts_list = Post.objects.filter(is_published=False, author=request.user).order_by('-created_at')
    draft_paginator = Paginator(draft_posts_list, 9)
    draft_page = request.GET.get('page', 1)

    try:
        draft_posts = draft_paginator.page(draft_page)
    except PageNotAnInteger:
        draft_posts = draft_paginator.page(1)
    except EmptyPage:
        draft_posts = draft_paginator.page(draft_paginator.num_pages)
    except:
        draft_posts = draft_paginator.page(1)

    profile = Profile.objects.get(user=request.user)

    return render(request, 'blog/dashboard/dashboard.html', {
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'profile': profile,
    })


@login_required
def dashboard_view_post(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/dashboard/dashboard-view-post.html', {'post': post})


@login_required
def dashboard_new_post(request):
    # ==================== DEBUG MODE ====================
    from django.conf import settings
    import sys

    print("\n" + "=" * 60)
    print("🔧 CLOUDINARY DEBUG INFO")
    print("=" * 60)
    print(f"📦 DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"🔑 CLOUDINARY_URL exists: {bool(getattr(settings, 'CLOUDINARY_URL', None))}")
    print(f"🔑 CLOUDINARY_URL value: {getattr(settings, 'CLOUDINARY_URL', 'NOT SET')[:50]}...")

    # Vérifier si cloudinary_storage est chargé
    print(f"📚 Apps installées contenant 'cloudinary':")
    for app in settings.INSTALLED_APPS:
        if 'cloudinary' in app.lower():
            print(f"   - {app}")

    # Vérifier l'ordre
    try:
        cs_index = settings.INSTALLED_APPS.index('cloudinary_storage')
        sf_index = settings.INSTALLED_APPS.index('django.contrib.staticfiles')
        c_index = settings.INSTALLED_APPS.index('cloudinary')
        print(f"\n📊 Ordre des apps:")
        print(f"   cloudinary_storage à l'index: {cs_index}")
        print(f"   staticfiles à l'index: {sf_index}")
        print(f"   cloudinary à l'index: {c_index}")
        print(f"   ✅ Ordre correct!" if cs_index < sf_index < c_index else "   ❌ ORDRE INCORRECT!")
    except ValueError as e:
        print(f"   ❌ ERREUR: Une app est manquante - {e}")

    print("=" * 60 + "\n")
    # ==================== FIN DEBUG ====================

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # ==================== DEBUG POST-SAVE ====================
            if post.image:
                print("\n" + "=" * 60)
                print("🖼️  IMAGE SAVED INFO")
                print("=" * 60)
                print(f"📁 Image name: {post.image.name}")
                print(f"🔗 Image URL: {post.image.url}")
                print(f"💾 Storage class: {post.image.storage.__class__.__name__}")
                print(f"📦 Storage module: {post.image.storage.__class__.__module__}")
                print("=" * 60 + "\n")
            # ==================== FIN DEBUG POST-SAVE ====================

            messages.success(request, 'Votre article a été enregistré.')
            return redirect('blog-dashboard')
    else:
        form = PostForm()
    return render(request, 'blog/dashboard/dashboard-new-post.html', {'form': form})


@login_required
def dashboard_edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    old_image = post.image.path if post.image else None

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            if 'image' in request.FILES:
                if old_image and os.path.exists(old_image):
                    os.remove(old_image)

            form.save()
            messages.success(request, "Votre article a été modifié.")
            return redirect('blog-dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/dashboard/dashboard-edit-post.html', {'form': form, 'post': post})


@login_required
def dashboard_delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        messages.error('Vous n\'êtes pas autorisé à supprimer cette article.')
        return redirect('blog-home')

    if request.method == 'POST':
        if post:
            if post.image:
                image_path = post.image.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            post.delete()
            messages.success(request, "Votre article a été supprimé.")
        else:
            messages.error(request, "Suppression impossible, veuillez recommencer.")
    return redirect('blog-dashboard')


@login_required
def dashboard_edit_profil(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été modifié avec succès.")
            return redirect('blog-dashboard')
    else:
        form = ProfileForm(instance=profile)

    return render(request, "blog/dashboard/dashboard-edit-profile.html", {'form': form})
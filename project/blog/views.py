import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect

from .forms.commentForm import CommentForm
from .forms.contactForm import ContactForm
from .forms.postForm import PostForm
from .forms.profileForm import ProfileForm
from .models import Post, Profile, Comment


# ------------------------
# Pages publiques
# ------------------------

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
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except Exception:
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
            comment.save()
            messages.success(request, 'Votre commentaire a été posté.')
            return redirect('blog-single-post', id=id)
    else:
        form = CommentForm()

    return render(request, 'blog/single-post.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Merci pour votre message. Nous vous répondrons dans les plus brefs délais.'
            )
            return redirect('blog-contact')
    else:
        form = ContactForm()

    return render(request, 'blog/contact.html', {'form': form})


# ------------------------
# Tableau de bord
# ------------------------

@login_required
def dashboard(request):
    published_posts_list = Post.objects.filter(
        is_published=True, author=request.user
    ).order_by('-created_at')

    published_paginator = Paginator(published_posts_list, 9)
    published_page = request.GET.get('page', 1)

    try:
        published_posts = published_paginator.page(published_page)
    except PageNotAnInteger:
        published_posts = published_paginator.page(1)
    except EmptyPage:
        published_posts = published_paginator.page(published_paginator.num_pages)
    except Exception:
        published_posts = published_paginator.page(1)

    draft_posts_list = Post.objects.filter(
        is_published=False, author=request.user
    ).order_by('-created_at')

    draft_paginator = Paginator(draft_posts_list, 9)
    draft_page = request.GET.get('page', 1)

    try:
        draft_posts = draft_paginator.page(draft_page)
    except PageNotAnInteger:
        draft_posts = draft_paginator.page(1)
    except EmptyPage:
        draft_posts = draft_paginator.page(draft_paginator.num_pages)
    except Exception:
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
    if request.method == 'POST':
        try:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()

                # Gestion des tags ManyToMany
                form.save_m2m()

                # Debug
                if post.image:
                    try:
                        print(f"✅ Image uploadée!")
                        print(f"📁 URL: {post.image.url}")
                    except Exception as e:
                        print(f"⚠️ Erreur lecture URL image: {e}")
                else:
                    print(f"❌ Pas d'image uploadée")

                messages.success(request, 'Votre article a été enregistré.')
                return redirect('blog-dashboard')
            else:
                messages.error(request, 'Erreur dans le formulaire. Vérifiez les champs.')
        except Exception as e:
            print(f"❌ Erreur création post: {e}")
            messages.error(request, f'Une erreur est survenue lors de la création de l\'article.')
            return redirect('blog-dashboard')
    else:
        form = PostForm()

    return render(request, 'blog/dashboard/dashboard-new-post.html', {'form': form})


@login_required
def dashboard_edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    # Sauvegarder l'ancienne image AVANT le traitement du formulaire
    old_image = None
    try:
        if post.image:
            old_image = post.image
    except Exception as e:
        print(f"⚠️ Erreur lecture ancienne image: {e}")

    if request.method == 'POST':
        try:
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                # Si une nouvelle image est uploadée, supprimer l'ancienne de Cloudinary
                if 'image' in request.FILES and old_image:
                    try:
                        old_image.delete(save=False)
                        print("✅ Ancienne image supprimée de Cloudinary")
                    except Exception as e:
                        print(f"⚠️ Impossible de supprimer l'ancienne image: {e}")

                form.save()
                messages.success(request, "Votre article a été modifié.")
                return redirect('blog-dashboard')
            else:
                messages.error(request, 'Erreur dans le formulaire. Vérifiez les champs.')
        except Exception as e:
            print(f"❌ Erreur modification post: {e}")
            messages.error(request, f'Une erreur est survenue lors de la modification.')
            return redirect('blog-dashboard')
    else:
        form = PostForm(instance=post)

    return render(
        request,
        'blog/dashboard/dashboard-edit-post.html',
        {'form': form, 'post': post},
    )


@login_required
def dashboard_delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cet article.")
        return redirect('blog-home')

    if request.method == 'POST':
        try:
            # Supprimer l'image de Cloudinary si elle existe
            if post.image:
                try:
                    post.image.delete(save=False)
                    print("✅ Image supprimée de Cloudinary")
                except Exception as e:
                    print(f"⚠️ Impossible de supprimer l'image: {e}")

            post.delete()
            messages.success(request, "Votre article a été supprimé.")
        except Exception as e:
            print(f"❌ Erreur suppression post: {e}")
            messages.error(request, "Une erreur est survenue lors de la suppression.")

        return redirect('blog-dashboard')

    return redirect('blog-dashboard')


@login_required
def dashboard_edit_profil(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        try:
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Votre profil a été modifié avec succès.")
                return redirect('blog-dashboard')
            else:
                messages.error(request, 'Erreur dans le formulaire. Vérifiez les champs.')
        except Exception as e:
            print(f"❌ Erreur modification profil: {e}")
            messages.error(request, "Une erreur est survenue lors de la modification du profil.")
            return redirect('blog-dashboard')
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "blog/dashboard/dashboard-edit-profile.html",
        {'form': form},
    )
'''
import os

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

    return render(request, 'blog/post.html', {'posts':posts})

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
    return render(request, 'blog/contact.html',{'form':form})

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
    return render(request, 'blog/dashboard/dashboard-view-post.html', {'post':post})


@login_required
def dashboard_new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            users = User.objects.all()
            if users.exists():
                post.author = request.user

            post.save()
            messages.success(request, 'Votre article a été enregistré.')
            return redirect('blog-dashboard')
    else:
        form = PostForm()
    return render(request, 'blog/dashboard/dashboard-new-post.html', {'form':form})


@login_required
def dashboard_edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    old_image = post.image.path if post.image else None  # garder l'ancienne image

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # Vérifie si une nouvelle image est uploadée
            if 'image' in request.FILES:
                # Supprimer l'ancienne seulement si elle existe
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
'''
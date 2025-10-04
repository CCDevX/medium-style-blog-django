#!/usr/bin/env python
import os
import django
import random
from faker import Faker

# Initialise Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Profile, Comment

fake = Faker("fr_FR")


def create_users(max_users=5):
    users = []
    for _ in range(max_users):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password="password123"
        )
        # Profil lié
        Profile.objects.create(
            user=user,
            description=fake.paragraph()
        )
        users.append(user)
    return users


def create_categories(max_categories=5):
    categories = []
    for _ in range(max_categories):
        categories.append(Category.objects.create(
            name=fake.word(),
            description=fake.sentence()
        ))
    return categories


def create_tags(max_tags=10):
    tags = []
    for _ in range(max_tags):
        tags.append(Tag.objects.create(
            name=fake.word(),
            description=fake.sentence()
        ))
    return tags


def create_posts(users, categories, tags, max_posts=50):
    posts = []
    for _ in range(max_posts):
        post = Post.objects.create(
            title=fake.sentence(nb_words=6),
            content=fake.paragraph(nb_sentences=50),
            is_published=True,
            author=random.choice(users),
            categories=random.choice(categories),
        )
        # Ajouter quelques tags
        post.tags.add(*random.sample(tags, k=random.randint(1, 3)))
        posts.append(post)
    return posts


def create_comments(users, posts, max_comments=20):
    for _ in range(max_comments):
        Comment.objects.create(
            content=fake.paragraph(nb_sentences=3),
            note=random.randint(1, 5),
            author=random.choice(users),
            post=random.choice(posts),
        )


if __name__ == "__main__":
    print("Suppression des anciennes données...")
    User.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Post.objects.all().delete()
    Profile.objects.all().delete()
    Comment.objects.all().delete()

    print("Création de données factices...")
    '''users = create_users()
    categories = create_categories()
    tags = create_tags()
    posts = create_posts(users, categories, tags)
    create_comments(users, posts)'''

    print("🎉 Base remplie avec succès !")

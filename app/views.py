from django.shortcuts import render, redirect, HttpResponse
from .models import Post, BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,  login, logout
from django.contrib import messages
from django.http import HttpResponse
import math


def bloghome(request):
    no_of_posts = 2
    #if request.GET("pageno")
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    allposts = Post.objects.all()
    length = len(allposts)
    allblog =  Post.objects.all()
    allposts = allposts[(page-1)*no_of_posts: page* no_of_posts]
    if page>1:
        prev = page - 1
    else:
        prev = None

    if page<math.ceil(length / no_of_posts):
        nxt = page + 1
    else: nxt = None
    
    context = {'allPosts': allposts, 'prev': prev, 'nxt': nxt, "allblog":allblog }
    return render(request, "app/post.html", context)

def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)

    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'app/search.html', params)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}

    return render(request, "app/blogPost.html", context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/{post.slug}/")
  


# Create your views here.
def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) < 5:
            messages.error(request, " Your user name must not be under 5 characters")
            return redirect('/')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('/')
        if pass1 != pass2:
            messages.error(request, " Passwords do not match")
            return redirect('/')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " Your mCoder has been successfully created")
        return redirect('/')

    else:
        return HttpResponse("404 - Not found")


def handeLogin(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['name']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")

    return HttpResponse("404- Not found")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

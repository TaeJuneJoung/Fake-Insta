from django.shortcuts import render, redirect
from .forms import PostForm, ImageForm, CommentForm
from .models import Post, Comment, Hashtag
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST #POST방식으로만 받겠다는 것, GET방식이면 405를 보냄

# Create your views here.
def list(request):
    posts = Post.objects.all().order_by('-id')
    #Comment를 작성할 수 있는 부분을 만들기
    comment_form = CommentForm()
    return render(request, "posts/index.html", {"posts":posts, "comment_form":comment_form})

@login_required
def new(request):
    # 4.사용자가 데이터를 입력해서
    #   POST방식으로 요청
    
    # 9.사용자가 다시 적절한 데이터를 입력해서 POST바익으로 요청
    if request.method == 'POST':
        # 5.POST방식으로 저장요청을 받고,
        #   데이터를 받아 PostForm에 넣어서 인스턴스화 한다.
        
        # 10.5번과 동일
        post_form = PostForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        # 6.데이터 검증
        
        # 11.6번과 동일
        if post_form.is_valid():
            # 7-1.데이터 검증 통과(이후 과정 없음 - 8번포함의 이후 작업 없음)
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            
            ###Hashtag 기능 추가 - post객체가 있고 m2m을 해야한다
            #is_valid()된 거에서 cleaned_data를 가져와서 접근하면 된다.
            content = post_form.cleaned_data.get('content')
            content_words = content.split()
            for word in content_words:
                if word[0] == "#":
                    tag = Hashtag.objects.get_or_create(content=word)#get_or_create -> 가져오거나 생성하거나
                    # if tag[1]: #이작업이 필요없음 알아서 해줌(?)
                    post.hashtags.add(tag[0])
            ###Hashtag 기능 끝
            
            #다중사진을 처리하기 위해 for문
            for image in request.FILES.getlist('img'):
                request.FILES['img'] = image
                image_form = ImageForm(request.POST, request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    #참조받는 image에 post위치를 알려줘야하기에
                    image.post = post
                    image.save()
            # 12-1. 적절한 데이터가 들어오고 데이터 저장후 list페이지 redirect
            return redirect("posts:list")
        else: #적지 않아도 되는데 학습상 명시적으로 보이기 위해 씀
            # 7-2.데이터 검증 실패(적절하지 않은 데이터가 들어올 때)
            pass
        
    # 1.GET방식 -> 데이터 입력할 form 요청
    else:
    # 2.PostForm을 인스턴스화 시켜 form에 저장
        post_form = PostForm()
        image_form = ImageForm()
    # 3.form을 담아서 new.html에 보내준다.
    
    # 8.사용자가 입력한 데이터를 form에 담아진 상태로 다시 form에 담아 new.html에 보내줌
    #   실수하였을 때 다시 그 모습 그대로 보여주기 위해 인텐트를 땅김
    return render(request, 'posts/form.html', {'post_form':post_form, "image_form":image_form})
    
@login_required
def update(request, id):
    post = Post.objects.get(pk=id)
    if post.user == request.user:
        if request.method == "POST":
            post_form = PostForm(request.POST, instance=post) #instance를 이용하여 update라는 것을 알려줌
            if post_form.is_valid():
                post = post_form.save()
                
                ###Hashtag 기능 추가 - post객체가 있고 m2m을 해야한다
                #update에서 이전의 것을 다 지우고 새로 만듬
                #tag[1]을 통해서 이전의것에서 분기처리해도 됨
                post.hashtags.clear()
                #is_valid()된 거에서 cleaned_data를 가져와서 접근하면 된다.
                content = post_form.cleaned_data.get('content')
                content_words = content.split()
                for word in content_words:
                    if word[0] == "#":
                        tag = Hashtag.objects.get_or_create(content=word)#get_or_create -> 가져오거나 생성하거나
                        # if tag[1]: #add인것을 보면 dict나 set이기에 중복시 되지 않으니 괜찮음.
                        post.hashtags.add(tag[0])
            ###Hashtag 기능 끝
                
                return redirect("posts:list")
        else:
            post_form = PostForm(instance=post)
        return render(request, 'posts/form.html', {'post_form':post_form})
    else:
        #올바르지 않은 접근
        return redirect("posts:list")
        
@login_required
def delete(request, id):
    post = Post.objects.get(pk=id)
    if post.user == request.user:
        post.delete()
    return redirect("posts:list")
    
@login_required
@require_POST
def comment_create(request, id):
    post = Post.objects.get(pk=id)
    # if request.method == "POST": #require_post라서 
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect("posts:list")
            
    # else: #list에서 바로 하기에 여기서는 처리하지 않음
    #     form = CommentForm()
    # return render(request, "", {"form":form})

@login_required
def comment_delete(request, id, c_id):
    comment = Comment.objects.get(pk=c_id)
    if comment.user == request.user:
        comment.delete()
    return redirect("posts:list")

@login_required
def like(request, id):
    user = request.user
    post = Post.objects.get(pk=id)
    # if 사용자가 좋아요를 안눌렀다면
        # 좋아요 추가
    # else 사용자가 좋아요를 이미 눌렀다면
        # 좋아요 취소
    
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    return redirect("posts:list")
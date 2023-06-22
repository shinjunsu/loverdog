from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


from .models import Post, Category, Tag, Comment
from .forms import CommentForm


class PostList(ListView):
    model = Post
    ordering = '-pk'
    paginate_by = 5
    # template_name = 'blog/post_list_ori.html'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context




# function base
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#     # blog 폴더 밑에있는 index.html을 호출해줘
#     # 화면을 templates 폴더 밑에 둔다.
#     return render(request, 'blog/post_list_ori.html', {'abc':posts})

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context


# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(request, 'blog/post_detail_ori.html',{"post":post})


    # get : 특정 조건을 만족하는 단일 객체를 반환
    # filter : 주어진 모든 조건을 만족하는 모든 객체를 반환
def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(request, 'blog/post_list.html',
                  { 'post_list' : post_list,
                    'categories' : Category.objects.all(),
                    'no_category_post_count' : Post.objects.filter(category=None).count(),
                    'category' : category
                  })


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()      # tag와 관련된 모든 post list를 가지고 온다.

    return render(request, 'blog/post_list.html',
    { 'post_list' : post_list,
      'category'  : Category.objects.all(),
      'no_category_post_count' : Post.objects.filter(category=None).count(),
      'tag' : tag
    })

class PostCreate(LoginRequiredMixin,CreateView):
    model = Post            # Post의 레코드를 사용할 수 있게 하는 기능
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):           # 로그인한 사용자 여부 체크
            form.instance.author = current_user
            result = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:        # tags가 있는 경우에만 처리
                tags_str = tags_str.strip()
                tags_str = tags_str.rstrip(';')
                tags_str = tags_str.replace(',',';')
                tags_list = tags_str.split(';') # list요소로 반환

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return result
        else :
            return redirect('/blog/')


class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    template_name = 'blog/post_update_form.html'


    def dispatch(self, request, *args, **kwargs):
        # 로그인 체크와 작성자 체크
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ";".join(tags_str_list)
        return context

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:  # tags가 있는 경우에만 처리
            tags_str = tags_str.strip()
            tags_str = tags_str.rstrip(';')
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')  # list요소로 반환

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response


def new_comment(request, pk):
    # 로그인 여부 확인
    if request.user.is_authenticated:
        # get_object_or_404 : 알맞지 않은 pk값이 넘어오면, 404 error 를 발생시킨다.
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            # 사용자로부터 제출된 데이터를 이용하여 CommentForm의 인스턴스를 생성
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():     # is_valid() : 폼 처리시 유효성 검사
                comment = comment_form.save(commit=False)   # 일단은 저장하지 않고
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())


        return redirect(post.get_absolute_url())

    else:
        return PermissionError


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment      # 업데이트할 모델 클래스를 지정
    form_class = CommentForm    # 사용할 폼 클래스를 지정

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author :
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else :
            return PermissionDenied


def delete_comment(request, pk):
    comment= get_object_or_404(Comment, pk=pk)
    post = comment.post

    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        return PermissionDenied


class PostSearch(PostList):
    paginate_by = None # PostList에는 정의되어 있지만, PostSearch에서는 정의하지 않는다.

    def get_queryset(self):
        # class 형에서 인자를 받아오는 방식
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search:{q} ({self.get_queryset().count()})'
        return context







from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import board
from django.utils import timezone

# Create your views here.

def index(request):
    """
    게시판 목록
    """
    board_list = board.objects.order_by('-create_date')
    context = {'board_list': board_list}
    return render(request, 'board/board_list.html', context)

def detail(request, board_id):
    """
    board_id에 따른 게시글 보기
    """
    board_detail = board.objects.get(id=board_id)
    context = {'board_detail': board_detail}
    return render(request, 'board/board_detail.html', context)

def comment_create(request, board_id):
    """
    댓글 등록
    """


+
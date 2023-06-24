from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:     # ModelForm의 메타데이터를 정의하는데 사용
        model = Comment
        fields = ('content', )      # 포함될 필드만 작성
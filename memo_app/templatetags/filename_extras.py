# memo_app/templatetags/filename_extras.py
from django import template
import os

register = template.Library()

@register.filter(name='filename')
def get_filename(value):
    """ファイルパスからファイル名のみを抽出するカスタムフィルター"""
    return os.path.basename(value)
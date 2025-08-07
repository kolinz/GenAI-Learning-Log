# memo_app/templatetags/markdown_extras.py
from django import template
from django.template.defaultfilters import stringfilter
import markdown as md

register = template.Library()

@register.filter
@stringfilter
def markdownify(text):
    """マークダウンテキストをHTMLに変換する"""
    return md.markdown(text, extensions=['fenced_code', 'extra', 'nl2br'])
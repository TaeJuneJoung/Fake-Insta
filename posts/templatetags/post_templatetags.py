#파일의 이름은 중요하지 않음. -> but, 폴더의 이름은 중요함
from django import template

register = template.Library()

@register.filter
def hashtag_link(post):
    content = post.content #content정보들
    hashtags = post.hashtags.all() #hashtag의 목록들 <Queryset [hashtag1, hashtag...]>
    
    content = content.split()
    for c in range(len(content)):
        for hashtag in hashtags:
            if content[c] == hashtag.content:
                content[c] = """<a href="{% url 'posts:hashtag' hashtag.id %}">"""+hashtag.content+"</a>"
    content = " ".join(content)
    
    return content
from django import template

register = template.Library()

BLOCKED_WORDS = (
    'дурачок', 'дурак', 'дебил', 'придурок'
)


@register.filter()
def censor(text):
    words = text.split(' ')
    list_text = []
    for word in words:
        if word.lower() in BLOCKED_WORDS:
            postfix = word[:1] + '*' * (len(word) - 1)
            list_text.append(postfix)
        else:
            list_text.append(word)
    return ' '.join(list_text)

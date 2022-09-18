from django import template

register = template.Library()

PROFANITIES = [
    'fuck',
    'shit',
    'bitch',
    'cunt',
    'whore',
    'редиска',
    'хуй',
    'пизда',
    'ебать',
    'жопа',
    'блядь',
]


@register.filter()
def censor(text):
    try:
        if not isinstance(text, str):
            raise TypeError('Censored text is not a string')
    except TypeError:
        print('Censored text is not of string type')
    else:
        wordlist = text.split()
        for i, j in enumerate(wordlist):
            if j.lower() in PROFANITIES:
                j = j[0] + '*' * (len(j) - 1)
                wordlist[i] = j
        return ' '.join(wordlist)

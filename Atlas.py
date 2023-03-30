from newspaper import Article

def article(url):
    article = Article(url, language="en")
    article.download()
    article.parse()
    article.nlp()
    return article.text


def wiki(lw):
    s = lw.split()
    st = ''
    for i in range(len(s)):
        st = st + '_' + s[i].title()
    st = st[1:]
    return 'https://en.wikipedia.org/wiki/' + st
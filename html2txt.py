# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, Tag, NavigableString
import htmlentitydefs, re
BLOD_LINE = re.compile(r"^\s*\*\*[\r\n]+", re.M)

_char = re.compile(r'&(\w+?);')
_dec = re.compile(r'&#(\d{2,4});')
_hex = re.compile(r'&#x(\d{2,4});')

def _char_unescape(m, defs=htmlentitydefs.entitydefs):
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0)


import re, htmlentitydefs
def unescape(s):
    # First convert alpha entities (such as &eacute;)
    # (Inspired from http://mail.python.org/pipermail/python-list/2007-June/443813.html)
    def entity2char(m):
        entity = m.group(1)
        if entity in htmlentitydefs.name2codepoint:
            return unichr(htmlentitydefs.name2codepoint[entity])
        return u" "  # Unknown entity: We replace with a space.
    t = re.sub(u'&(%s);' % u'|'.join(htmlentitydefs.name2codepoint), entity2char, s)

    # Then convert numerical entities (such as &#233;)
    t = re.sub(u'&#(\d+);', lambda x: unichr(int(x.group(1))), t)

    # Then convert hexa entities (such as &#x00E9;)
    return re.sub(u'&#x(\w+);', lambda x: unichr(int(x.group(1), 16)), t)


BLOCK_BOLD = set([
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
])

BLOCK = set([
    'form',
    'hr',
    'div',
    'table',
    'tr',
    'li',
    'pre',
    'p',
])

BOLD = set([
    'b',
    'strong',
    'i',
    'em',
])

PASS = set([
    'span',
    'font',
])

def html2txt(htm):
    htm = htm.replace(u'*', u'﹡').replace('\r\n', '\n').replace('\r', '\n')

    soup = BeautifulSoup(htm)


    def soup2txt_rtursion(soup):
        li = []
        for i in soup:

            if isinstance(i, NavigableString):

                li.append(i.string)

            else:

                name = i.name
                if name == 'a':
                    s = soup2txt_rtursion(i)
                    ss = s.rstrip()

                    href = i.get('href') or ''
                    if href not in ss:
                        li.append(ss)
                        if href and href.startswith('http') and href != ss:
                            li.append('[[%s]]'%href)
                        li.append(s[len(ss):])
                    else:
                        li.append(s)
                elif name == 'img':
                    src = i.get('src')
                    if src:
                        #img_url = upyun_fetch_pic(src)
                        li.append(u'\n图:%s\n' % src)
                elif name == 'pre':
                    s = soup2txt_rtursion(i)
                    if s:
                        if '\n' in s.strip('\n') and (len(s.encode('utf-8', 'ignore'))/len(s)) < 2:
                            s = '\n{{{\r%s\r}}}\n'%s.replace('\n', '\r').strip('\r')
                        li.append(s)
                else:
                    s = soup2txt_rtursion(i)

                    if name in BLOCK_BOLD :
                        if '\n' not in s and '**' not in s:
                            li.append(u'\n**%s**\n' % s)
                        else:
                            li.append(s)
                    elif name in BLOCK:
                        li.append(u'\n%s\n' % s)
                    elif name in BOLD and '**' not in s and '\n' not in s:
                        li.append(u'**%s**' % s)
                    else:
                        li.append(s)

        return u''.join(li)

    s = soup2txt_rtursion(soup)
    s = unescape(s.strip())
    txt = s
    txt = '\n\n'.join(filter(bool, [i.strip() for i in s.split('\n')]))
    txt = txt.replace('\r', '\n')
    txt = BLOD_LINE.sub('**', txt)
    return txt

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print html2txt("""
ss
<pre class="brush: python">
# coding: utf-8
<a href="http://w/po/10264458" target="_blank" class="txt_title_a">慢慢的，我们长成了受困于数字的大人</a>
class A(object):
我我
我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我
我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我
我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我 我我
    @property
    def _value(self):
#        raise AttributeError(&quot;test&quot;)
        return {&quot;v&quot;: &quot;This is a test.&quot;}

    def __getattr__(self, key):
        print &quot;__getattr__:&quot;, key
        return self._value[key]

if __name__ == &#39;__main__&#39;:
    a = A()
    print a.v


</pre>s
""")
    print unescape("""<option value='&#20013;&#22269;&#35821;&#35328;&#25991;&#23398;&#31995;'>&#20013;&#22269;&#35821;&#35328;&#25991;&#23398;&#31995;</option>""")


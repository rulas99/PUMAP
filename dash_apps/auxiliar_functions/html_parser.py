from bs4 import BeautifulSoup
import dash_html_components as html
from re import sub


def html_to_dash(p1):
    p1 = p1.replace('\n','').strip()
    p1 = sub(r'\  +','',p1)
    el = BeautifulSoup(p1, "html.parser")
    
    res = []
    for i in el.contents:
        if 'href' in i.attrs:
            res.append(getattr(html,i.name.title())(i.contents[0],href=i.attrs["href"],style={'color': '#1C71F4'},target="_blank"))
        else:
            res.append(getattr(html,i.name.title())(i.contents[0]))

    return res
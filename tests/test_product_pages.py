import unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
PAGES={'zh-Hant':'japan-menu-guide/index.html','en':'japan-menu-guide/en/index.html','ja':'japan-menu-guide/ja/index.html'}
class HTML(HTMLParser):
 def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class ProductPages(unittest.TestCase):
 def test_studio_and_product_pages_have_working_navigation_and_content(self):
  self.assertTrue((ROOT/'index.html').is_file(),'Studio homepage must resolve')
  for lang,path in PAGES.items():
   with self.subTest(lang=lang):
    text=(ROOT/path).read_text();html=HTML(text)
    self.assertIn(('html',{'lang':lang}),html.tags)
    self.assertEqual(sum(tag=='h1' for tag,_ in html.tags),1)
    links=[a.get('href','') for tag,a in html.tags if tag=='a'];self.assertTrue(any('apps.apple.com/' in x and '6826183208' in x for x in links));self.assertTrue(any('/privacy' in x for x in links))
    self.assertEqual({a['hreflang'] for tag,a in html.tags if tag=='a' and 'hreflang' in a},set(PAGES))
    self.assertNotIn('googletagmanager',text);self.assertNotIn('google-analytics',text)
    for tag,a in html.tags:
     for field in ['href','src']:
      u=a.get(field,'');parsed=urlsplit(u)
      if not u or parsed.scheme or not parsed.path:continue
      target=(ROOT/parsed.path.lstrip('/')) if parsed.path.startswith('/') else ROOT/path/ '..'/parsed.path
      target=target.resolve();self.assertTrue(target.is_relative_to(ROOT));self.assertTrue(target.exists(),str(target))
 def test_translation_system_requirement_is_explicit(self):
  for path in PAGES.values():
   text=(ROOT/path).read_text()
   self.assertGreaterEqual(text.count("iOS / iPadOS 18"),2,path)
 def test_existing_seller_authorization_is_unchanged(self):
  self.assertEqual((ROOT/'app-ads.txt').read_text().strip(),'google.com, pub-2131017108269082, DIRECT, f08c47fec0942fa0')
if __name__=='__main__':unittest.main()

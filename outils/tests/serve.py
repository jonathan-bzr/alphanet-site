#!/usr/bin/env python3
"""Serveur local qui imite Cloudflare Pages, pour les tests :
/page.html -> redirection 308 vers /page, /page -> page.html, adresse inconnue -> 404.html (statut 404).
Usage : python3 outils/tests/serve.py [port]   (à la racine du dépôt ; port 8766 par défaut)"""
import http.server, os, sys
from urllib.parse import urlsplit

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        u = urlsplit(self.path)
        p = u.path
        q = ('?' + u.query) if u.query else ''
        if p.endswith('.html') and os.path.isfile('.' + p):
            new = p[:-len('index.html')] if p.endswith('/index.html') else p[:-5]
            self.send_response(308); self.send_header('Location', new + q); self.end_headers(); return
        if p != '/' and not os.path.splitext(p)[1] and os.path.isfile('.' + p + '.html'):
            self.path = p + '.html' + q
        elif not os.path.exists('.' + p):
            body = open('404.html', 'rb').read()
            self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body); return
        super().do_GET()
    do_HEAD = do_GET

if __name__ == '__main__':
    http.server.ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1]) if len(sys.argv) > 1 else 8766), Handler).serve_forever()

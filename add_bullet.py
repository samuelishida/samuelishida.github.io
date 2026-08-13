#!/usr/bin/env python3
"""Add new Goldman Sachs bullet to all MD and HTML files."""

import os

BASE_DIR = r"e:\Code\github-pages-cv"

NEW_BULLET_MD = "- Built a production support AI agent leveraging RAG and GitHub Copilot.\n"
NEW_BULLET_HTML = '                                <li>Built a production support AI agent leveraging RAG and GitHub Copilot.</li>\n'

OLD_BULLET_MD = "- Built AI-assisted docs tool with RAG, using OpenAI's API running in a VPS.\n"
OLD_BULLET_HTML = "                                <li>Built AI-assisted docs tool with RAG, using OpenAI's API running in a VPS.</li>\n"

# MD files
md_files = ['cv.md','cv_ai_platform.md','cv_genai.md','cv_backend.md','cv_bespoke.md','cv_uber_auth.md']
for f in md_files:
    fp = os.path.join(BASE_DIR, f)
    with open(fp, encoding='utf-8') as fh:
        c = fh.read()
    if OLD_BULLET_MD in c:
        c = c.replace(OLD_BULLET_MD, NEW_BULLET_MD + OLD_BULLET_MD)
        with open(fp, 'w', encoding='utf-8') as fh:
            fh.write(c)
        print(f'{f}: OK')
    else:
        print(f'{f}: NOT FOUND')

# HTML variant files
html_files = ['cv_ai_platform.html','cv_genai.html','cv_backend.html','cv_bespoke.html','cv_uber_auth.html']
for f in html_files:
    fp = os.path.join(BASE_DIR, f)
    with open(fp, encoding='utf-8') as fh:
        c = fh.read()
    if OLD_BULLET_HTML in c:
        c = c.replace(OLD_BULLET_HTML, NEW_BULLET_HTML + OLD_BULLET_HTML)
        with open(fp, 'w', encoding='utf-8') as fh:
            fh.write(c)
        print(f'{f}: OK')
    else:
        print(f'{f}: NOT FOUND')

# index.html
fp = os.path.join(BASE_DIR, 'index.html')
with open(fp, encoding='utf-8') as fh:
    c = fh.read()

old_html = '<li data-i18n="sre_desc1">Built AI-assisted docs tool with RAG, using OpenAI\'s API running in a VPS.</li>\n'
new_html = '<li data-i18n="sre_desc_new">Built a production support AI agent leveraging RAG and GitHub Copilot.</li>\n' + old_html

if old_html in c:
    c = c.replace(old_html, new_html)

    # EN i18n
    old_en = '"sre_desc1": "Built AI-assisted docs tool with RAG, using OpenAI\'s API running in a VPS."'
    new_en = '"sre_desc_new": "Built a production support AI agent leveraging RAG and GitHub Copilot.",\n                ' + old_en
    c = c.replace(old_en, new_en)

    # PT i18n
    old_pt = '"sre_desc1": "Arquitetou uma ferramenta de documenta\u00e7\u00e3o assistida por IA, permitindo consultas conversacionais para engenheiros de suporte e usu\u00e1rios de neg\u00f3cios."'
    new_pt = '"sre_desc_new": "Construiu um agente de IA para suporte de produ\u00e7\u00e3o utilizando RAG e GitHub Copilot.",\n                ' + old_pt
    c = c.replace(old_pt, new_pt)

    with open(fp, 'w', encoding='utf-8') as fh:
        fh.write(c)
    print('index.html: OK')
else:
    print('index.html: NOT FOUND')

print('\nDone!')

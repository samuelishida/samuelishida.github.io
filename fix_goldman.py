#!/usr/bin/env python3
"""Update Goldman Sachs descriptions in all HTML files."""

import os

BASE_DIR = r"e:\Code\github-pages-cv"

# Variant HTMLs: replace first two bullets with new first bullet
OLD_VARIANT = (
    '                                <li>Built a production support AI agent leveraging RAG and GitHub Copilot.</li>\n'
    '                                <li>Built AI-assisted docs tool with RAG, using OpenAI\'s API running in a VPS.</li>\n'
    '                                <li>Migrated internal Apache servers from RHEL 7 to RHEL 8, producing documentation for other clusters to follow</li>\n'
    '                                <li>Collaborated with the Strats team to optimize infrastructure used for risk curves and pricing models.</li>\n'
    '                                <li>Delivered trainings on GitHub Copilot and AI-assisted workflows.</li>'
)

NEW_VARIANT = (
    '                                <li>Built a production support AI tool to query internal documentation and live logs, with RAG and GitHub Copilot.</li>\n'
    '                                <li>Migrated internal Apache servers from RHEL 7 to RHEL 8, producing documentation for other clusters to follow</li>\n'
    '                                <li>Collaborated with the Strats team to optimize infrastructure used for risk curves and pricing models.</li>\n'
    '                                <li>Delivered trainings on GitHub Copilot and AI-assisted workflows.</li>'
)

# index.html body
OLD_INDEX_BODY = (
    '                                <li data-i18n="sre_desc_new">Built a production support AI agent leveraging RAG and GitHub Copilot.</li>\n'
    '                                <li data-i18n="sre_desc1">Built AI-assisted docs tool with RAG, using OpenAI\'s API running in a VPS.</li>\n'
    '                                <li data-i18n="sre_desc2">Migrated internal Apache servers from RHEL 7 to RHEL 8, producing documentation for other clusters to follow</li>\n'
    '                                <li data-i18n="sre_desc3">Collaborated with the Strats team to optimize infrastructure used for risk curves and pricing models.</li>\n'
    '                                <li data-i18n="sre_desc4">Delivered trainings on GitHub Copilot and AI-assisted workflows.</li>'
)

NEW_INDEX_BODY = (
    '                                <li data-i18n="sre_desc_new">Built a production support AI tool to query internal documentation and live logs, with RAG and GitHub Copilot.</li>\n'
    '                                <li data-i18n="sre_desc2">Migrated internal Apache servers from RHEL 7 to RHEL 8, producing documentation for other clusters to follow</li>\n'
    '                                <li data-i18n="sre_desc3">Collaborated with the Strats team to optimize infrastructure used for risk curves and pricing models.</li>\n'
    '                                <li data-i18n="sre_desc4">Delivered trainings on GitHub Copilot and AI-assisted workflows.</li>'
)

# index.html EN i18n
OLD_EN_I18N = (
    '                "sre_desc_new": "Built a production support AI agent leveraging RAG and GitHub Copilot.",\n'
    '                "sre_desc1": "Built AI-assisted docs tool with RAG, using OpenAI\'s API running in a VPS.",\n'
    '                "sre_desc2": "Migrated internal Apache servers from RHEL 7 to RHEL 8, producing documentation for other clusters to follow",\n'
    '                "sre_desc3": "Collaborated with the Strats team to optimize infrastructure used for risk curves and pricing models.",\n'
    '                "sre_desc4": "Delivered trainings on GitHub Copilot and AI-assisted workflows.",'
)

NEW_EN_I18N = (
    '                "sre_desc_new": "Built a production support AI tool to query internal documentation and live logs, with RAG and GitHub Copilot.",\n'
    '                "sre_desc2": "Migrated internal Apache servers from RHEL 7 to RHEL 8, producing documentation for other clusters to follow",\n'
    '                "sre_desc3": "Collaborated with the Strats team to optimize infrastructure used for risk curves and pricing models.",\n'
    '                "sre_desc4": "Delivered trainings on GitHub Copilot and AI-assisted workflows.",'
)

# index.html PT i18n
OLD_PT_I18N = (
    '                "sre_desc_new": "Construiu um agente de IA para suporte de produ\u00e7\u00e3o utilizando RAG e GitHub Copilot.",\n'
    '                "sre_desc1": "Construiu uma ferramenta de documenta\u00e7\u00e3o assistida por IA com RAG, usando a API da OpenAI rodando em um VPS.",\n'
    '                "sre_desc2": "Migrou servidores Apache internos do RHEL 7 para o RHEL 8, produzindo documenta\u00e7\u00e3o para outros clusters seguirem",\n'
    '                "sre_desc3": "Colaborou com a equipe de Strats para otimizar a infraestrutura usada para curvas de risco e modelos de precifica\u00e7\u00e3o.",\n'
    '                "sre_desc4": "Ministrou treinamentos sobre GitHub Copilot e fluxos de trabalho assistidos por IA.",'
)

NEW_PT_I18N = (
    '                "sre_desc_new": "Construiu uma ferramenta de IA para suporte de produ\u00e7\u00e3o para consultar documenta\u00e7\u00e3o interna e logs em tempo real, com RAG e GitHub Copilot.",\n'
    '                "sre_desc2": "Migrou servidores Apache internos do RHEL 7 para o RHEL 8, produzindo documenta\u00e7\u00e3o para outros clusters seguirem",\n'
    '                "sre_desc3": "Colaborou com a equipe de Strats para otimizar a infraestrutura usada para curvas de risco e modelos de precifica\u00e7\u00e3o.",\n'
    '                "sre_desc4": "Ministrou treinamentos sobre GitHub Copilot e fluxos de trabalho assistidos por IA.",'
)


def main():
    # Variant HTMLs
    for fname in ['cv_ai_platform.html', 'cv_genai.html', 'cv_backend.html', 'cv_bespoke.html', 'cv_uber_auth.html']:
        fp = os.path.join(BASE_DIR, fname)
        with open(fp, encoding='utf-8') as f:
            c = f.read()
        if OLD_VARIANT in c:
            c = c.replace(OLD_VARIANT, NEW_VARIANT)
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f'{fname}: OK')
        else:
            print(f'{fname}: NOT FOUND')

    # index.html
    fp = os.path.join(BASE_DIR, 'index.html')
    with open(fp, encoding='utf-8') as f:
        c = f.read()

    changes = 0
    if OLD_INDEX_BODY in c:
        c = c.replace(OLD_INDEX_BODY, NEW_INDEX_BODY)
        changes += 1
    else:
        print('index.html body: NOT FOUND')

    if OLD_EN_I18N in c:
        c = c.replace(OLD_EN_I18N, NEW_EN_I18N)
        changes += 1
    else:
        print('index.html EN i18n: NOT FOUND')

    if OLD_PT_I18N in c:
        c = c.replace(OLD_PT_I18N, NEW_PT_I18N)
        changes += 1
    else:
        print('index.html PT i18n: NOT FOUND')

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'index.html: {changes} changes')

    print('\nDone!')


if __name__ == '__main__':
    main()

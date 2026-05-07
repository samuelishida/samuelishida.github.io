import re

# Read index.html as template
with open('index.html', 'r', encoding='utf-8') as f:
    template = f.read()

# CV to HTML mapping: cv file -> html file, subtitle
mappings = [
    ('cv_ai_platform.md', 'cv_ai_platform.html', 'AI Platform Engineer'),
    ('cv_genai.md', 'cv_genai.html', 'Senior AI Engineer'),
    ('cv_backend.md', 'cv_backend.html', 'Senior Software Engineer'),
    ('cv_bespoke.md', 'cv_bespoke.html', 'Senior Backend & DevOps Engineer'),
    ('cv_uber_auth.md', 'cv_uber_auth.html', 'Software Engineer | DevSecOps'),
]

# Company logo URLs
COMPANY_LOGOS = {
    'Goldman Sachs': 'https://media.licdn.com/dms/image/v2/D4E0BAQG9L7InIQVZrQ/company-logo_100_100/company-logo_100_100/0/1722506756452/goldman_sachs_logo?e=1779321600&v=beta&t=br1hASPJXeBzWgxCKPLetiP6k47KfolKYXKcFkuty7E',
    'Alctel Telecom': 'https://media.licdn.com/dms/image/v2/C4D0BAQEGzpjuQOQuFw/company-logo_100_100/company-logo_100_100/0/1630433013891/alctel_logo?e=1779321600&v=beta&t=xX2nvBomnzv_ddAJJoUKBliIoWBrMVeXwGJ76F4hNUU',
    'GFT Group': 'https://media.licdn.com/dms/image/v2/D4E0BAQFS8Oq_RoTX9Q/company-logo_100_100/B4EZmE9ECUIUAQ-/0/1758872224292/gft_technologies_logo?e=1779321600&v=beta&t=Tcf9QtphP6AM5DuBF-e2ig7BXX_JEmFZWIX0G1inAV4',
    'Suma': 'https://media.licdn.com/dms/image/v2/C4D0BAQGYIJKBpVfk6w/company-logo_100_100/company-logo_100_100/0/1654033713354/sumaconnect_logo?e=1779321600&v=beta&t=fqSN59v79PX3qjrPzr2pNJU46gCdybasJjw-p3QSAVE',
    'Bit Capital': 'bitcapital-icon.png',
    'Boilesen Associates': 'https://media.licdn.com/dms/image/v2/D4D0BAQE7GIxYxDhmsg/company-logo_100_100/B4DZnjEaquJUAQ-/0/1760451210272/boilesen_logo?e=1779321600&v=beta&t=qjuVR2ppvvDAunSelQwkTOUlVhbKelz8Stg4UEhJX-Y',
    'Stoom': 'https://media.licdn.com/dms/image/v2/D4D0BAQHh4TSJtPM07A/company-logo_100_100/B4DZ3QF0wAH8AQ-/0/1777312681695/stoom_ecommerce_logo?e=1779321600&v=beta&t=5tq5jluijiARCsfCG3W38naJbifPzvyELvDfeZTAh4Y',
}

def get_logo(company_name):
    for key, url in COMPANY_LOGOS.items():
        if key.lower() in company_name.lower():
            return url
    return ''

def md_to_html(text):
    """Convert markdown bold (**text**) to HTML <strong>text</strong>"""
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

def strip_bullet(text):
    """Remove leading '- ' from bullet points"""
    if text.startswith('- '):
        return text[2:]
    return text

def parse_cv(content):
    """Parse markdown CV into sections"""
    result = {'summary': '', 'skills': [], 'experience': [], 'education': [], 'certs': [], 'languages': []}
    
    lines = content.split('\n')
    current_section = None
    current_exp = None
    
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith('## Professional Summary'):
            current_section = 'summary'
            continue
        elif stripped.startswith('## Technical Skills'):
            current_section = 'skills'
            continue
        elif stripped.startswith('## Professional Experience'):
            current_section = 'experience'
            continue
        elif stripped.startswith('## Education'):
            current_section = 'education'
            continue
        elif stripped.startswith('## Certifications'):
            current_section = 'certs'
            continue
        elif stripped.startswith('## Languages'):
            current_section = 'languages'
            continue
        elif stripped.startswith('## Contact') or stripped.startswith('# '):
            current_section = None
            continue
        
        if current_section == 'summary':
            if stripped and not stripped.startswith('##'):
                result['summary'] += stripped + ' '
        elif current_section == 'skills':
            if stripped.startswith('**') and ':**' in stripped:
                skills_text = stripped.split(':**', 1)[1].strip()
                for skill in skills_text.split(','):
                    skill = skill.strip()
                    if skill:
                        result['skills'].append(skill)
        elif current_section == 'experience':
            if stripped.startswith('### '):
                header = stripped.replace('### ', '').strip()
                result['experience'].append({'header': header, 'date': '', 'bullets': []})
                current_exp = result['experience'][-1]
            elif stripped.startswith('*') and current_exp and not current_exp['date']:
                current_exp['date'] = stripped.strip('*').strip()
            elif stripped.startswith('- ') and current_exp:
                current_exp['bullets'].append(strip_bullet(stripped))
        elif current_section == 'education':
            if stripped.startswith('- **'):
                result['education'].append(md_to_html(stripped.strip('- ').strip()))
        elif current_section == 'certs':
            if stripped.startswith('- **'):
                result['certs'].append(md_to_html(stripped.strip('- ').strip()))
        elif current_section == 'languages':
            if stripped.startswith('- **'):
                result['languages'].append(md_to_html(stripped.strip('- ').strip()))
    
    return result

def build_html(template, cv_data, subtitle):
    html = template
    
    # Update title tag
    html = re.sub(r'<title>.*?</title>', f'<title>Samuel Toyoshi Ishida \u2014 {subtitle}</title>', html)
    
    # Update subtitle in header
    html = re.sub(r'<div class="subtitle">.*?</div>', f'<div class="subtitle">{subtitle}</div>', html)
    
    # Update summary
    summary = cv_data['summary'].strip()
    html = re.sub(
        r'<p class="summary-text" data-i18n="summary_text">.*?</p>',
        f'<p class="summary-text" data-i18n="summary_text">{summary}</p>',
        html, flags=re.DOTALL
    )
    
    # Update skills
    skills_html = '\n'.join([f'                    <span class="skill-item">{s}</span>' for s in cv_data['skills']])
    skills_pattern = r'(<div class="skills-list">)\n.*?\n(                </div>)'
    html = re.sub(skills_pattern, rf'\1\n{skills_html}\n\2', html, flags=re.DOTALL)
    
    # Update experience with logos
    exp_items = []
    for job in cv_data['experience']:
        logo_url = get_logo(job['header'])
        bullets_html = '\n'.join([f'                                <li>{b}</li>' for b in job['bullets']])
        exp_items.append(f'''                <div class="experience-item">
                    <div class="exp-layout">
                        <div class="exp-logo">
                            <img src="{logo_url}" alt="" loading="lazy">
                        </div>
                        <div class="exp-body">
                            <div class="experience-header">
                                <h3>{job['header']}</h3>
                                <div class="job-meta">
                                    <span>{job['date']}</span>
                                </div>
                            </div>
                            <ul>
{bullets_html}
                            </ul>
                        </div>
                    </div>
                </div>''')
    
    exp_section = '\n\n'.join(exp_items)
    
    # Replace experience section (between experience_title h2 and projects_title h2)
    exp_pattern = r'(<h2 data-i18n="experience_title">.*?</h2>)\s*\n\s*.*?\n(\s*</section>\s*\n\s*<section>\s*\n\s*<h2 data-i18n="projects_title">)'
    replacement = rf'\1\n\n{exp_section}\n\n            \2'
    html = re.sub(exp_pattern, replacement, html, flags=re.DOTALL)
    
    # Update education
    edu_items = '\n'.join([f'                    <div class="education-item"><div><span class="degree">{e}</span></div></div>' for e in cv_data['education']])
    edu_pattern = r'(<div class="education-list">)\n.*?\n(                </div>)'
    html = re.sub(edu_pattern, rf'\1\n{edu_items}\n\2', html, flags=re.DOTALL)
    
    # Update certs
    cert_items = '\n'.join([f'                    <li>{c}</li>' for c in cv_data['certs']])
    cert_pattern = r'(<h2 data-i18n="certs_title">.*?</h2>\s*\n\s*<ul class="cert-list">)\n.*?\n(\s*</ul>)'
    html = re.sub(cert_pattern, rf'\1\n{cert_items}\n\2', html, flags=re.DOTALL)
    
    # Update languages
    lang_items = '\n'.join([f'                    <li>{l}</li>' for l in cv_data['languages']])
    lang_pattern = r'(<h2 data-i18n="languages_title">.*?</h2>\s*\n\s*<ul class="cert-list">)\n.*?\n(\s*</ul>)'
    html = re.sub(lang_pattern, rf'\1\n{lang_items}\n\2', html, flags=re.DOTALL)
    
    return html

for cv_file, html_file, subtitle in mappings:
    with open(cv_file, 'r', encoding='utf-8') as f:
        cv_content = f.read()
    
    cv_data = parse_cv(cv_content)
    html = build_html(template, cv_data, subtitle)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Generated: {html_file}')

print('All HTMLs updated!')

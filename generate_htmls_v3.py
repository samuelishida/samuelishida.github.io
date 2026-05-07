import re
import os

def parse_markdown_cv(filepath):
    """Parse a markdown CV file into structured data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    data = {
        'title': '',
        'name': 'Samuel Toyoshi Ishida',
        'role': '',
        'contact': {},
        'summary': '',
        'skills': [],
        'experience': [],
        'education': [],
        'certifications': [],
        'languages': []
    }
    
    # Extract title
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if title_match:
        data['title'] = title_match.group(1)
        parts = data['title'].split(' — ')
        data['name'] = parts[0].strip()
        data['role'] = parts[1].strip() if len(parts) > 1 else 'Software Engineer'
    
    # Extract contact info
    contact_section = re.search(r'## Contact\r?\n\r?\n(.+?)(?=\r?\n##)', content, re.DOTALL)
    if contact_section:
        contact_text = contact_section.group(1)
        for line in contact_text.strip().split('\r\n'):
            if 'Email:' in line:
                match = re.search(r'\*\*Email:\*\* (.+)', line)
                if match:
                    data['contact']['email'] = match.group(1)
            elif 'LinkedIn:' in line:
                match = re.search(r'\*\*LinkedIn:\*\* (.+)', line)
                if match:
                    data['contact']['linkedin'] = match.group(1)
            elif 'Location:' in line:
                match = re.search(r'\*\*Location:\*\* (.+)', line)
                if match:
                    data['contact']['location'] = match.group(1)
    
    # Extract summary
    summary_match = re.search(r'## Professional Summary\r?\n\r?\n(.+?)(?=\r?\n##)', content, re.DOTALL)
    if summary_match:
        data['summary'] = summary_match.group(1).strip()
    
    # Extract skills
    skills_match = re.search(r'## Technical Skills\r?\n\r?\n(.+?)(?=\r?\n##)', content, re.DOTALL)
    if skills_match:
        skills_text = skills_match.group(1)
        for line in skills_text.split('\r\n'):
            if line.startswith('**') and ':**' in line:
                cat_match = re.match(r'\*\*(.+?):\*\*\s*(.+)', line)
                if cat_match:
                    category = cat_match.group(1)
                    items_text = cat_match.group(2)
                    items = []
                    current = ''
                    depth = 0
                    for char in items_text:
                        if char == '(':
                            depth += 1
                            current += char
                        elif char == ')':
                            depth -= 1
                            current += char
                        elif char == ',' and depth == 0:
                            items.append(current.strip())
                            current = ''
                        else:
                            current += char
                    if current.strip():
                        items.append(current.strip())
                    data['skills'].append({'category': category, 'items': items})
    
    # Extract experience - improved parsing
    exp_section = re.search(r'## Professional Experience\r?\n\r?\n(.+?)(?=\r?\n##)', content, re.DOTALL)
    if exp_section:
        exp_text = exp_section.group(1)
        # Split by ### headers
        exp_items = re.split(r'\r?\n### ', exp_text)
        for item in exp_items:
            item = item.strip()
            if not item:
                continue
            lines = item.split('\r\n')
            header = lines[0]
            # Parse header: Company — Title
            header_match = re.match(r'(.+?) — (.+)', header)
            if header_match:
                company = header_match.group(1).strip()
                title = header_match.group(2).strip()
            else:
                company = header
                title = ''
            
            period = ''
            desc_lines = []
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                if re.match(r'\*\w+ \d{4} –', line) or re.match(r'\*\w+ \d{4} – \w+ \d{4}', line) or re.match(r'\*\w+ \d{4} – Present', line):
                    period = line.strip('*').strip()
                elif line.startswith('- '):
                    desc_lines.append(line[2:].strip())
            
            data['experience'].append({
                'company': company,
                'title': title,
                'period': period,
                'descriptions': desc_lines
            })
    
    # Extract education
    edu_section = re.search(r'## Education\r?\n\r?\n(.+?)(?=\r?\n##)', content, re.DOTALL)
    if edu_section:
        edu_text = edu_section.group(1)
        for line in edu_text.split('\r\n'):
            if line.startswith('- '):
                edu_match = re.search(r'\*\*(.+?)\*\* — (.+?) \((.+?)\)', line)
                if edu_match:
                    data['education'].append({
                        'degree': edu_match.group(1),
                        'school': edu_match.group(2),
                        'dates': edu_match.group(3)
                    })
    
    # Extract certifications
    cert_section = re.search(r'## Certifications \u0026 Highlights\r?\n\r?\n(.+?)(?=\r?\n##|$)', content, re.DOTALL)
    if cert_section:
        cert_text = cert_section.group(1)
        for line in cert_text.split('\r\n'):
            if line.startswith('- '):
                data['certifications'].append(line[2:].strip())
    
    # Extract languages
    lang_section = re.search(r'## Languages\r?\n\r?\n(.+?)(?=\r?\n##|$)', content, re.DOTALL)
    if lang_section:
        lang_text = lang_section.group(1)
        for line in lang_text.split('\r\n'):
            if line.startswith('- '):
                data['languages'].append(line[2:].strip())
    
    return data

def generate_html(data, output_path):
    """Generate HTML CV from data."""
    
    # Build skills HTML
    skills_html = ''
    for skill_cat in data['skills']:
        for item in skill_cat['items']:
            skills_html += f'                    <span class="skill-item">{item}</span>\n'
    
    # Build experience HTML
    experience_html = ''
    for exp in data['experience']:
        experience_html += f'''                <div class="experience-item">
                    <div class="exp-layout">
                        <div class="exp-body">
                            <div class="experience-header">
                                <h3>{exp['title']}</h3>
                                <div class="job-meta">
                                    <span>{exp['period']}</span>
                                </div>
                            </div>
                            <div class="job-company"><span class="company">{exp['company']}</span></div>
                            <ul>
'''
        for desc in exp['descriptions']:
            experience_html += f'                                <li>{desc}</li>\n'
        experience_html += '''                            </ul>
                        </div>
                    </div>
                </div>

'''
    
    # Build education HTML
    education_html = ''
    for edu in data['education']:
        education_html += f'''                    <div class="education-item">
                        <div>
                            <span class="degree">{edu['degree']}</span>
                            <span class="school"> · {edu['school']}</span>
                        </div>
                        <span class="dates">{edu['dates']}</span>
                    </div>
'''
    
    # Build languages HTML
    languages_html = ''
    for lang in data['languages']:
        languages_html += f'                    <li>{lang}</li>\n'
    
    # Build certifications HTML
    certifications_html = ''
    for cert in data['certifications']:
        certifications_html += f'                    <li>{cert}</li>\n'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name']} — {data['role']}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300;1,9..40,400&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #fafaf9;
            --surface: #ffffff;
            --ink: #0a0a0a;
            --ink-secondary: #44403c;
            --ink-tertiary: #78716c;
            --ink-faint: #a8a29e;
            --accent: #9f4a34;
            --accent-light: #fdf2ef;
            --rule: #e7e5e4;
            --rule-strong: #d6d3d1;
            --shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.06);
            --transition: color 0.2s ease, background 0.2s ease;
        }}

        html[data-theme="dark"] {{
            --bg: #0c0a09;
            --surface: #1c1917;
            --ink: #f5f5f4;
            --ink-secondary: #d6d3d1;
            --ink-tertiary: #a8a29e;
            --ink-faint: #78716c;
            --accent: #d9775e;
            --accent-light: #2a1b15;
            --rule: #292524;
            --rule-strong: #44403c;
            --shadow: 0 1px 3px rgba(0,0,0,0.3), 0 8px 24px rgba(0,0,0,0.4);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        html {{ scroll-behavior: smooth; }}

        body {{
            font-family: "DM Sans", sans-serif;
            background: var(--bg);
            color: var(--ink);
            line-height: 1.6;
            font-weight: 400;
            font-size: 15px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            transition: var(--transition);
        }}

        .page {{
            max-width: 860px;
            margin: 0 auto;
            background: var(--surface);
            min-height: 100vh;
            transition: var(--transition);
        }}

        header {{
            padding: 3.5rem 3.5rem 2.5rem;
            border-bottom: 1px solid var(--rule);
        }}

        .header-grid {{
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 2rem;
            align-items: baseline;
        }}

        .header-left h1 {{
            font-family: "DM Serif Display", serif;
            font-size: 2.6rem;
            font-weight: 400;
            color: var(--accent);
            letter-spacing: -0.02em;
            line-height: 1.05;
            margin-bottom: 0.4rem;
        }}

        .header-left .subtitle {{
            font-size: 0.95rem;
            color: var(--ink-secondary);
            font-weight: 500;
            letter-spacing: 0.02em;
        }}

        .header-right {{
            text-align: right;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }}

        .header-right a,
        .header-right span {{
            color: var(--ink-tertiary);
            text-decoration: none;
            font-size: 0.82rem;
            font-weight: 400;
            transition: color 0.15s;
        }}

        .header-right a:hover {{ color: var(--accent); }}

        .cv-body {{
            padding: 2.5rem 3.5rem 3.5rem;
        }}

        section {{
            margin-bottom: 2.2rem;
        }}

        section:last-child {{ margin-bottom: 0; }}

        h2 {{
            font-family: "DM Sans", sans-serif;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--ink-faint);
            margin-bottom: 1.2rem;
            padding-bottom: 0.6rem;
            border-bottom: 1px solid var(--rule);
        }}

        .summary-text {{
            font-size: 0.95rem;
            color: var(--ink-secondary);
            line-height: 1.75;
            font-weight: 400;
            max-width: 680px;
        }}

        .skills-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.15rem 0.6rem;
            font-size: 0.88rem;
            color: var(--ink-secondary);
            line-height: 1.8;
        }}

        .skills-list .skill-item {{
            white-space: nowrap;
        }}

        .skills-list .skill-item::after {{
            content: "·";
            margin-left: 0.6rem;
            color: var(--ink-faint);
        }}

        .skills-list .skill-item:last-child::after {{
            content: none;
        }}

        .experience-item {{
            margin-bottom: 1.6rem;
            padding-bottom: 1.6rem;
            border-bottom: 1px solid var(--rule);
            page-break-inside: avoid;
        }}

        .experience-item:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}

        .exp-layout {{
            display: flex;
            gap: 1rem;
            align-items: flex-start;
        }}

        .exp-body {{
            flex: 1;
            min-width: 0;
        }}

        .job-company {{
            font-size: 0.85rem;
            color: var(--ink-secondary);
            font-weight: 500;
            margin-top: 0.1rem;
            margin-bottom: 0.5rem;
        }}

        .experience-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 1rem;
            flex-wrap: wrap;
            margin-bottom: 0.6rem;
        }}

        .experience-header h3 {{
            font-family: "DM Sans", sans-serif;
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--ink);
            line-height: 1.3;
        }}

        .job-meta {{
            font-size: 0.82rem;
            color: var(--ink-tertiary);
            font-weight: 400;
            white-space: nowrap;
        }}

        .experience-item ul {{
            margin-left: 1.1rem;
            color: var(--ink-secondary);
            font-size: 0.88rem;
            line-height: 1.7;
        }}

        .experience-item li {{
            margin-bottom: 0.4rem;
        }}

        .experience-item li::marker {{
            color: var(--ink-faint);
        }}

        .education-list {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .education-item {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .education-item .degree {{
            font-weight: 500;
            color: var(--ink);
            font-size: 0.92rem;
        }}

        .education-item .school {{
            color: var(--ink-tertiary);
            font-size: 0.82rem;
        }}

        .education-item .dates {{
            color: var(--ink-faint);
            font-size: 0.82rem;
            font-style: italic;
        }}

        .cert-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        .cert-list li {{
            font-size: 0.88rem;
            color: var(--ink-secondary);
            line-height: 1.6;
            padding-left: 1.2rem;
            position: relative;
        }}

        .cert-list li::before {{
            content: "—";
            position: absolute;
            left: 0;
            color: var(--ink-faint);
            font-weight: 300;
        }}

        .print-btn {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: var(--ink);
            color: var(--surface);
            border: none;
            padding: 0.7rem 1.2rem;
            border-radius: 8px;
            cursor: pointer;
            font-family: "DM Sans", sans-serif;
            font-size: 0.8rem;
            font-weight: 600;
            box-shadow: var(--shadow);
            transition: all 0.2s ease;
            z-index: 100;
            letter-spacing: 0.02em;
        }}

        .print-btn:hover {{
            transform: translateY(-1px);
            opacity: 0.85;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}

        header, section {{
            animation: fadeIn 0.5s ease both;
        }}

        .cv-body section:nth-child(1) {{ animation-delay: 0.06s; }}
        .cv-body section:nth-child(2) {{ animation-delay: 0.12s; }}
        .cv-body section:nth-child(3) {{ animation-delay: 0.18s; }}
        .cv-body section:nth-child(4) {{ animation-delay: 0.24s; }}
        .cv-body section:nth-child(5) {{ animation-delay: 0.30s; }}
        .cv-body section:nth-child(6) {{ animation-delay: 0.36s; }}

        @media (max-width: 700px) {{
            body {{ font-size: 14px; }}
            header {{ padding: 4rem 1.5rem 2rem; }}
            .header-grid {{ grid-template-columns: 1fr; gap: 1rem; }}
            .header-right {{ text-align: left; }}
            .header-left h1 {{ font-size: 2rem; }}
            .cv-body {{ padding: 1.75rem 1.5rem 2.5rem; }}
            .experience-header {{ flex-direction: column; gap: 0.2rem; }}
            .exp-logo {{ width: 36px; height: 36px; }}
            .exp-logo img {{ width: 36px; height: 36px; }}
        }}

        @media print {{
            @page {{ size: A4; margin: 16mm 18mm; }}
            * {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            html, body {{ background: #fff !important; font-size: 12.5px; }}
            .print-btn {{ display: none !important; }}
            .page {{ max-width: 100% !important; box-shadow: none !important; background: #fff !important; }}
            header {{ padding: 1.5rem 0 1.25rem !important; animation: none !important; opacity: 1 !important; }}
            .header-left h1 {{ font-size: 2rem !important; color: #9f4a34 !important; }}
            .cv-body {{ padding: 1.25rem 0 2rem !important; }}
            section {{ opacity: 1 !important; transform: none !important; animation: none !important; margin-bottom: 1.4rem !important; }}
            .experience-item {{ margin-bottom: 1rem !important; padding-bottom: 1rem !important; page-break-inside: avoid; }}
            .education-item {{ page-break-inside: avoid; }}
            h2 {{ margin-bottom: 0.9rem !important; }}
            .experience-item ul {{ font-size: 0.82rem !important; }}
            .summary-text {{ font-size: 0.85rem !important; }}
            a {{ color: inherit !important; text-decoration: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="page">
        <header>
            <div class="header-grid">
                <div class="header-left">
                    <h1>{data['name']}</h1>
                    <div class="subtitle">{data['role']}</div>
                </div>
                <div class="header-right">
                    <a href="mailto:{data['contact'].get('email', '')}">{data['contact'].get('email', '')}</a>
                    <a href="https://{data['contact'].get('linkedin', '')}" target="_blank">{data['contact'].get('linkedin', '')}</a>
                    <span>{data['contact'].get('location', '')}</span>
                </div>
            </div>
        </header>

        <div class="cv-body">
            <section>
                <h2>Professional Summary</h2>
                <p class="summary-text">
                    {data['summary']}
                </p>
            </section>

            <section>
                <h2>Technical Skills</h2>
                <div class="skills-list">
{skills_html}                </div>
            </section>

            <section>
                <h2>Professional Experience</h2>

{experience_html}            </section>

            <section>
                <h2>Education</h2>
                <div class="education-list">
{education_html}                </div>
            </section>

            <section>
                <h2>Languages</h2>
                <ul class="cert-list">
{languages_html}                </ul>
            </section>

            <section>
                <h2>Certifications & Highlights</h2>
                <ul class="cert-list">
{certifications_html}                </ul>
            </section>
        </div>
    </div>

    <button class="print-btn" onclick="window.print()">Print / Save PDF</button>
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Generated: {output_path}")

# Process all CV files
cv_files = [
    ('cv_ai_platform.md', 'cv_ai_platform.html'),
    ('cv_genai.md', 'cv_genai.html'),
    ('cv_backend.md', 'cv_backend.html'),
    ('cv_bespoke.md', 'cv_bespoke.html'),
    ('cv_uber_auth.md', 'cv_uber_auth.html')
]

base_dir = r'e:\Code\github-pages-cv'

for md_file, html_file in cv_files:
    md_path = os.path.join(base_dir, md_file)
    html_path = os.path.join(base_dir, html_file)
    
    if os.path.exists(md_path):
        data = parse_markdown_cv(md_path)
        generate_html(data, html_path)
    else:
        print(f"File not found: {md_path}")

print("Done!")

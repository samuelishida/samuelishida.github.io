#!/usr/bin/env python3
"""Update all HTML CV files with new job descriptions. Preserves job titles."""

import os

BASE_DIR = r"e:\Code\github-pages-cv"

VARIANT_FILES = [
    "cv_ai_platform.html",
    "cv_genai.html",
    "cv_backend.html",
    "cv_bespoke.html",
    "cv_uber_auth.html",
]

# Each replacement is (old_string, new_string)
REPLACEMENTS = []

# Goldman Sachs
REPLACEMENTS.append((
    '<li>Built AI-assisted docs tool w/ RAG. Conversational queries for support/business on FICC.</li>\n'
    '                                <li>Deployed an automated web reporting solution.</li>\n'
    '                                <li>Built LLM pipelines (OpenAI + VPS) for knowledge retrieval.</li>\n'
    '                                <li>Collaborated with Strats/Quant team to enhance critical infrastructure.</li>\n'
    '                                <li>Delivered training on GitHub Copilot and AI-assisted workflows.</li>',
    '<li>Built AI-assisted docs tool with RAG, using OpenAI\'s API running in a VPS.</li>\n'
    '                                <li>Migrated internal Apache servers from RHEL 7 to RHEL 8, producing documentation for other clusters to follow</li>\n'
    '                                <li>Collaborated with the Strats team to optimize infrastructure used for risk curves and pricing models.</li>\n'
    '                                <li>Delivered trainings on GitHub Copilot and AI-assisted workflows.</li>'
))

# Alctel
REPLACEMENTS.append((
    '<li>Integrated chatbot solutions with WhatsApp using C#.</li>\n'
    '                                <li>Managed MySQL databases to ensure data integrity and performance.</li>\n'
    '                                <li>Provided technical support to resolve production issues.</li>',
    '<li>Gathered client business requirements and integrated chatbot solutions with WhatsApp using C#, .NET and MySQL.</li>\n'
    '                                <li>Provided technical support to resolve production issues.</li>'
))

# GFT
REPLACEMENTS.append((
    '<li>Led migration of 200 on-premise applications to AWS. Enhanced operational efficiency, reduced infrastructure costs.</li>\n'
    '                                <li>Implemented automation solutions: reduced processing time weeks \u2192 days (Terraform, CI/CD).</li>\n'
    '                                <li>Collaborated with international GFT team on automating document generation and backend service deployments.</li>',
    '<li>Led the migration of 200 on-premise applications to AWS using CloudFormation.</li>\n'
    '                                <li>Collaborated with the international team to automate document generation using Terraform and Python.</li>'
))

# Suma
REPLACEMENTS.append((
    '<li>Developed Django backend with ML integration for telemetry from truck sensors. Enabled predictive maintenance models.</li>\n'
    '                                <li>Built ETL pipelines: ingested, preprocessed large-scale sensor data for route optimization.</li>\n'
    '                                <li>Managed cloud data warehouse (Azure). Implemented feature engineering pipelines, integrated PowerBI for AI operational insights and anomaly detection.</li>',
    '<li>Built ETL pipelines to ingest and preprocess large scale sensor data, preparing datasets for route optimization.</li>\n'
    '                                <li>Integrated low-latency UDP communication protocols from custom-built telemetry sensors with SUMA servers.</li>\n'
    '                                <li>Managed a cloud data warehouse on Azure, engineering pipelines and integrating with PowerBI for AI-driven insights via Power BI.</li>'
))

# Bit Capital
REPLACEMENTS.append((
    '<li>Developed TypeScript APIs for blockchain-based digital banking platform.</li>\n'
    '                                <li>Reduced transaction intermediaries to improve efficiency.</li>',
    '<li>Developed high performance APIs in TypeScript to be used in credit cards transacions.</li>\n'
    '                                <li>Worked in the integration with Pix system</li>'
))

# Boilesen
REPLACEMENTS.append((
    '<li>Developed digital marketing tool for lead generation and tracking using PHP and Slim framework.</li>\n'
    '                                <li>Provided client support for Android Java applications, enhancing user experience.</li>',
    '<li>Developed a digital marketing tool for lead generation and tracking using PHP and the Slim framework.</li>\n'
    '                                <li>Provided client support for Android Java applications, enhancing user experience and satisfaction.</li>'
))

# Stoom
STOOM_OLD = '<li>Developed Suprevida e-commerce website using Apache Struts 2, Java, and JSP in an agile team environment.</li>'
STOOM_NEW = (
    '<li>Developed the Suprevida website using Apache Struts 2 and PostgreSQL.</li>\n'
    '                                <li>Collaborated with the team to address client demands and gather business requirements.</li>\n'
    '                                <li>Assisted in feature development and issue resolution for Brazil\'s leading retailer of domestic animal products.</li>'
)

# Devnup block to insert
DEVNUP_BLOCK = (
    '\n'
    '                <div class="experience-item">\n'
    '                    <div class="exp-layout">\n'
    '                        <div class="exp-logo">\n'
    '                            <img src="https://media.licdn.com/dms/image/v2/D4D0BAQHh4TSJtPM07A/company-logo_100_100/B4DZ3QF0wAH8AQ-/0/1777312681695/stoom_ecommerce_logo?e=1779321600&v=beta&t=5tq5jluijiARCsfCG3W38naJbifPzvyELvDfeZTAh4Y" alt="" loading="lazy">\n'
    '                        </div>\n'
    '                        <div class="exp-body">\n'
    '                            <div class="experience-header">\n'
    '                                <h3>Devnup IT Solutions \u2014 Software Engineer Intern</h3>\n'
    '                                <div class="job-meta">\n'
    '                                    <span>Jul 2017 \u2013 Dec 2017 \u00b7 6 mos</span>\n'
    '                                </div>\n'
    '                            </div>\n'
    '                            <ul>\n'
    '                                <li>Developed a sports distribution platform, Matchup Sports, utilizing Play, Spring, and AngularJS at Devnup IT Solutions.</li>\n'
    '                                <li>Enhanced platform functionality and user experience through skills in Springboot, Git, Docker, Java, and AngularJS.</li>\n'
    '                            </ul>\n'
    '                        </div>\n'
    '                    </div>\n'
    '                </div>'
)

STOOM_CLOSING = (
    '                            </ul>\n'
    '                        </div>\n'
    '                    </div>\n'
    '                </div>\n'
    '\n'
    '                        </section>'
)

STOOM_CLOSING_NEW = (
    '                            </ul>\n'
    '                        </div>\n'
    '                    </div>\n'
    '                </div>'
    + DEVNUP_BLOCK +
    '\n\n                        </section>'
)


def process_variant(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = 0

    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            changes += 1
        else:
            print(f"  WARN: block not found in {os.path.basename(filepath)}: {old[:80]}...")

    if STOOM_OLD in content:
        content = content.replace(STOOM_OLD, STOOM_NEW)
        changes += 1
    else:
        print(f"  WARN: Stoom not found in {os.path.basename(filepath)}")

    if STOOM_CLOSING in content:
        content = content.replace(STOOM_CLOSING, STOOM_CLOSING_NEW)
        changes += 1
    else:
        print(f"  WARN: Stoom closing not found in {os.path.basename(filepath)}")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  OK {os.path.basename(filepath)}: {changes} changes")
    else:
        print(f"  - {os.path.basename(filepath)}: no changes")


def process_index():
    filepath = os.path.join(BASE_DIR, "index.html")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = 0

    # EN i18n replacements
    en_reps = [
        ('"sre_desc1": "Architected an AI-assisted documentation tool, enabling conversational queries for support engineers and business users."',
         '"sre_desc1": "Built AI-assisted docs tool with RAG, using OpenAI\'s API running in a VPS."'),
        ('"sre_desc2": "Deployed a web-based reporting solution, significantly improving accessibility and operational efficiency for stakeholders."',
         '"sre_desc2": "Migrated internal Apache servers from RHEL 7 to RHEL 8, producing documentation for other clusters to follow"'),
        ('"sre_desc3": "Collaborated with Strats/Quant team to enhance critical infrastructure."',
         '"sre_desc3": "Collaborated with the Strats team to optimize infrastructure used for risk curves and pricing models."'),
        ('"sre_desc4": "Delivered training on GitHub Copilot and AI-assisted workflows, enhancing productivity for production support engineers."',
         '"sre_desc4": "Delivered trainings on GitHub Copilot and AI-assisted workflows."'),
        ('"alctel_desc1": "Integrated chatbot solutions with WhatsApp using C#, enhancing user engagement and accessibility."',
         '"alctel_desc1": "Gathered client business requirements and integrated chatbot solutions with WhatsApp using C#, .NET and MySQL."'),
        ('"alctel_desc2": "Managed MySQL databases to ensure data integrity and performance."',
         '"alctel_desc2": "Provided technical support to resolve production issues."'),
        ('"gft_desc1": "Led the migration of 200 on-premise applications to AWS, enhancing operational efficiency."',
         '"gft_desc1": "Led the migration of 200 on-premise applications to AWS using CloudFormation."'),
        ('"gft_desc2": "Implemented automation solutions that reduced processing time from weeks to days."',
         '"gft_desc2": "Collaborated with the international team to automate document generation using Terraform and Python."'),
        ('"suma_desc1": "Developed a Django backend for processing telemetry data from freight truck sensors."',
         '"suma_desc1": "Built ETL pipelines to ingest and preprocess large scale sensor data, preparing datasets for route optimization."'),
        ('"suma_desc2": "Built ETL pipelines to ingest on SUMA\'s stack, utilizing truck driver fuel receipts for gas price mapping."',
         '"suma_desc2": "Integrated low-latency UDP communication protocols from custom-built telemetry sensors with SUMA servers."'),
        ('"suma_desc3": "Managed a cloud data warehouse on Azure, integrating it with PowerBI for enhanced dashboards and operational reporting."',
         '"suma_desc3": "Managed a cloud data warehouse on Azure, engineering pipelines and integrating with PowerBI for AI-driven insights via Power BI."'),
        ('"bit_desc": "Developed APIs in TypeScript for a blockchain-based digital banking platform."',
         '"bit_desc": "Developed high performance APIs in TypeScript to be used in credit cards transacions."'),
        ('"bit_desc2": "Focused on reducing intermediaries involved in transactions to improve efficiency."',
         '"bit_desc2": "Worked in the integration with Pix system"'),
        ('"stoom_desc": "Developed the Suprevida website using Apache Struts 2, enhancing user experience for Stoom\'s customers."',
         '"stoom_desc": "Developed the Suprevida website using Apache Struts 2 and PostgreSQL."'),
        ('"stoom_desc2": "Collaborated with a team to address client demands and improve overall functionality."',
         '"stoom_desc2": "Collaborated with the team to address client demands and gather business requirements."'),
    ]

    for old, new in en_reps:
        if old in content:
            content = content.replace(old, new)
            changes += 1
        else:
            print(f"  WARN: index EN not found: {old[:80]}...")

    # Remove alctel_desc3
    old_a3 = '"alctel_desc3": "Provided technical support to resolve production issues, ensuring high client satisfaction.",\n'
    if old_a3 in content:
        content = content.replace(old_a3, "")
        changes += 1

    # Remove gft_desc3
    old_g3 = '"gft_desc3": "Collaborated with the international team at GFT Group to automate document generation.",\n'
    if old_g3 in content:
        content = content.replace(old_g3, "")
        changes += 1

    # Add Devnup if not present
    if "Devnup" not in content:
        # Insert Devnup HTML block after Stoom
        stoom_close = (
            '                            </ul>\n'
            '                            </div>\n'
            '                    </div>\n'
            '                </div>\n'
            '\n'
            '                        </section>'
        )
        devnup_html = (
            '\n'
            '                <div class="experience-item">\n'
            '                    <div class="exp-layout">\n'
            '                        <div class="exp-logo">\n'
            '                            <img src="https://media.licdn.com/dms/image/v2/D4D0BAQHh4TSJtPM07A/company-logo_100_100/B4DZ3QF0wAH8AQ-/0/1777312681695/stoom_ecommerce_logo?e=1779321600&v=beta&t=5tq5jluijiARCsfCG3W38naJbifPzvyELvDfeZTAh4Y" alt="Devnup IT Solutions" loading="lazy">\n'
            '                        </div>\n'
            '                        <div class="exp-body">\n'
            '                            <div class="experience-header">\n'
            '                                <h3 data-i18n="devnup_title">Software Engineer Intern</h3>\n'
            '                                <div class="job-meta">\n'
            '                                    <span data-i18n="devnup_period">Jul 2017 \u2013 Dec 2017 \u00b7 6 mos</span>\n'
            '                                </div>\n'
            '                            </div>\n'
            '                            <div class="job-company"><span class="company" data-i18n="devnup">Devnup IT Solutions</span></div>\n'
            '                            <ul>\n'
            '                                <li data-i18n="devnup_desc1">Developed a sports distribution platform, Matchup Sports, utilizing Play, Spring, and AngularJS at Devnup IT Solutions.</li>\n'
            '                                <li data-i18n="devnup_desc2">Enhanced platform functionality and user experience through skills in Springboot, Git, Docker, Java, and AngularJS.</li>\n'
            '                            </ul>\n'
            '                            </div>\n'
            '                    </div>\n'
            '                </div>'
        )
        if stoom_close in content:
            new_stoom = stoom_close.replace('</section>', devnup_html + '\n\n                        </section>')
            content = content.replace(stoom_close, new_stoom)
            changes += 1

        # Add EN i18n keys
        en_devnup = (
            ',\n'
            '                "devnup_title": "Software Engineer Intern",\n'
            '                "devnup_period": "Jul 2017 \u2013 Dec 2017 \u00b7 6 mos",\n'
            '                "devnup": "Devnup IT Solutions",\n'
            '                "devnup_desc1": "Developed a sports distribution platform, Matchup Sports, utilizing Play, Spring, and AngularJS at Devnup IT Solutions.",\n'
            '                "devnup_desc2": "Enhanced platform functionality and user experience through skills in Springboot, Git, Docker, Java, and AngularJS."'
        )
        en_close = (
            ',\n'
            '                "stoom_desc3": "Assisted in feature development and issue resolution for Brazil\'s leading retailer of domestic animal products."\n'
            '            },'
        )
        if en_close in content:
            content = content.replace(en_close, en_close.replace('}', en_devnup + '\n            }'))
            changes += 1

        # Add PT i18n keys
        pt_devnup = (
            ',\n'
            '                "devnup_title": "Estagi\u00e1rio em Engenharia de Software",\n'
            '                "devnup_period": "Jul 2017 \u2013 Dez 2017 \u00b7 6 meses",\n'
            '                "devnup": "Devnup IT Solutions",\n'
            '                "devnup_desc1": "Desenvolveu uma plataforma de distribui\u00e7\u00e3o esportiva, Matchup Sports, utilizando Play, Spring e AngularJS na Devnup IT Solutions.",\n'
            '                "devnup_desc2": "Aprimorou a funcionalidade e experi\u00eancia do usu\u00e1rio da plataforma utilizando Springboot, Git, Docker, Java e AngularJS."'
        )
        pt_close = (
            ',\n'
            '                "stoom_desc3": "Auxiliou no desenvolvimento de funcionalidades e resolu\u00e7\u00e3o de problemas para o maior varejista brasileiro de produtos para animais dom\u00e9sticos."\n'
            '            }'
        )
        if pt_close in content:
            content = content.replace(pt_close, pt_close.replace('}', pt_devnup + '\n            }'))
            changes += 1

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  OK index.html: {changes} changes")
    else:
        print(f"  - index.html: no changes")


def main():
    print("=== Variant HTMLs ===")
    for filename in VARIANT_FILES:
        filepath = os.path.join(BASE_DIR, filename)
        if os.path.exists(filepath):
            process_variant(filepath)

    print("\n=== index.html ===")
    process_index()

    print("\nDone!")


if __name__ == "__main__":
    main()

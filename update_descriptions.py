#!/usr/bin/env python3
"""Update all CV markdown files with new job descriptions. Preserves job titles."""

import os

BASE_DIR = r"e:\Code\github-pages-cv"

FILES = [
    "cv.md",
    "cv_ai_platform.md",
    "cv_genai.md",
    "cv_backend.md",
    "cv_bespoke.md",
    "cv_uber_auth.md",
]

# Map: old bullet block -> new bullet block
REPLACEMENTS = {
    # Goldman Sachs
    """- Built AI-assisted docs tool w/ RAG. Conversational queries for support/business on FICC.
- Deployed an automated web reporting solution.
- Built LLM pipelines (OpenAI + VPS) for knowledge retrieval.
- Collaborated with Strats/Quant team to enhance critical infrastructure.
- Delivered training on GitHub Copilot and AI-assisted workflows.""": 
    """- Built AI-assisted docs tool with RAG, using OpenAI's API running in a VPS.
- Migrated internal Apache servers from RHEL 7 to RHEL 8, producing documentation for other clusters to follow
- Collaborated with the Strats team to optimize infrastructure used for risk curves and pricing models.
- Delivered trainings on GitHub Copilot and AI-assisted workflows.""",

    # Alctel Telecom
    """- Integrated chatbot solutions with WhatsApp using C#.
- Managed MySQL databases to ensure data integrity and performance.
- Provided technical support to resolve production issues.""":
    """- Gathered client business requirements and integrated chatbot solutions with WhatsApp using C#, .NET and MySQL.
- Provided technical support to resolve production issues.""",

    # GFT Group
    """- Led migration of 200 on-premise applications to AWS. Enhanced operational efficiency, reduced infrastructure costs.
- Implemented automation solutions: reduced processing time weeks → days (Terraform, CI/CD).
- Collaborated with international GFT team on automating document generation and backend service deployments.""":
    """- Led the migration of 200 on-premise applications to AWS using CloudFormation.
- Collaborated with the international team to automate document generation using Terraform and Python.""",

    # Suma
    """- Developed Django backend with ML integration for telemetry from truck sensors. Enabled predictive maintenance models.
- Built ETL pipelines: ingested, preprocessed large-scale sensor data for route optimization.
- Managed cloud data warehouse (Azure). Implemented feature engineering pipelines, integrated PowerBI for AI operational insights and anomaly detection.""":
    """- Built ETL pipelines to ingest and preprocess large scale sensor data, preparing datasets for route optimization.
- Integrated low-latency UDP communication protocols from custom-built telemetry sensors with SUMA servers.
- Managed a cloud data warehouse on Azure, engineering pipelines and integrating with PowerBI for AI-driven insights via Power BI.""",

    # Bit Capital
    """- Developed TypeScript APIs for blockchain-based digital banking platform.
- Reduced transaction intermediaries to improve efficiency.""":
    """- Developed high performance APIs in TypeScript to be used in credit cards transacions.
- Worked in the integration with Pix system""",

    # Boilesen Associates
    """- Developed digital marketing tool for lead generation and tracking using PHP and Slim framework.
- Provided client support for Android Java applications, enhancing user experience.""":
    """- Developed a digital marketing tool for lead generation and tracking using PHP and the Slim framework.
- Provided client support for Android Java applications, enhancing user experience and satisfaction.""",
}

# Stoom + Devnup insertion (two variants: with/without blank line before ## Education)
STOOM_DEVNUP_OLD_WITH_BLANK = """- Developed Suprevida e-commerce website using Apache Struts 2, Java, and JSP in an agile team environment.

## Education"""

STOOM_DEVNUP_OLD_WITHOUT_BLANK = """- Developed Suprevida e-commerce website using Apache Struts 2, Java, and JSP in an agile team environment.
## Education"""

STOOM_DEVNUP_NEW = """- Developed the Suprevida website using Apache Struts 2 and PostgreSQL.
- Collaborated with the team to address client demands and gather business requirements.
- Assisted in feature development and issue resolution for Brazil's leading retailer of domestic animal products.

### Devnup IT Solutions — Software Engineer Intern
*Jul 2017 – Dec 2017 · 6 mos*

- Developed a sports distribution platform, Matchup Sports, utilizing Play, Spring, and AngularJS at Devnup IT Solutions.
- Enhanced platform functionality and user experience through skills in Springboot, Git, Docker, Java, and AngularJS.

## Education"""


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = 0

    # Apply standard replacements
    for old, new in REPLACEMENTS.items():
        if old in content:
            content = content.replace(old, new)
            changes += 1
        else:
            print(f"  WARNING: old block not found in {os.path.basename(filepath)}")
            print(f"  Old block preview: {old[:80]}...")

    # Handle Stoom + Devnup
    if STOOM_DEVNUP_OLD_WITH_BLANK in content:
        content = content.replace(STOOM_DEVNUP_OLD_WITH_BLANK, STOOM_DEVNUP_NEW)
        changes += 1
    elif STOOM_DEVNUP_OLD_WITHOUT_BLANK in content:
        content = content.replace(STOOM_DEVNUP_OLD_WITHOUT_BLANK, STOOM_DEVNUP_NEW)
        changes += 1
    else:
        print(f"  WARNING: Stoom block not found in {os.path.basename(filepath)}")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ {os.path.basename(filepath)}: {changes} replacements applied")
    else:
        print(f"  - {os.path.basename(filepath)}: no changes")


def main():
    for filename in FILES:
        filepath = os.path.join(BASE_DIR, filename)
        if os.path.exists(filepath):
            process_file(filepath)
        else:
            print(f"  SKIP: {filename} not found")

    print("\nDone!")


if __name__ == "__main__":
    main()

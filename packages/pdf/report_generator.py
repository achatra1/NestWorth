# /packages/pdf/report_generator.py
import os
from jinja2 import Environment, FileSystemLoader


# Set up Jinja2 environment to load templates from the templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)


def generate_pdf_report(blueprint, report_id):
    """Render the blueprint into a PDF file and return the file path.

    Args:
        blueprint: BabyBudgetBlueprint object
        report_id: Unique identifier for this report (UUID or string)

    Returns:
        String path to the generated PDF file
    """
    try:
        from weasyprint import HTML
    except ImportError:
        # Graceful fallback if WeasyPrint is not available
        print("Warning: WeasyPrint not installed. Generating HTML only.")
        return generate_html_report(blueprint, report_id)

    template = env.get_template("blueprint_report.html")
    html_content = template.render(blueprint=blueprint)

    # Define output PDF path
    output_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "pdfs")
    os.makedirs(output_dir, exist_ok=True)

    pdf_path = os.path.join(output_dir, f"baby_budget_blueprint_{report_id}.pdf")

    # Render PDF
    HTML(string=html_content).write_pdf(pdf_path)

    return pdf_path


def generate_html_report(blueprint, report_id):
    """Render the blueprint into an HTML file (fallback if PDF generation fails).

    Args:
        blueprint: BabyBudgetBlueprint object
        report_id: Unique identifier for this report (UUID or string)

    Returns:
        String path to the generated HTML file
    """
    template = env.get_template("blueprint_report.html")
    html_content = template.render(blueprint=blueprint)

    # Define output HTML path
    output_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "pdfs")
    os.makedirs(output_dir, exist_ok=True)

    html_path = os.path.join(output_dir, f"baby_budget_blueprint_{report_id}.html")

    # Write HTML file
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return html_path

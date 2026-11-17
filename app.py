!pip install gradio PyPDF2
import gradio as gr
import PyPDF2
import re

skills_list = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "Excel",
    "Communication",
    "Teamwork",
    "React",
    "Django",
    "Flask",
    "AWS",
    "Power BI"
]

def extract_resume_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def analyze_resume(pdf_file, job_description):

    if pdf_file is None:
        return "Please upload your resume.", "", "", ""

    if not job_description.strip():
        return "Please enter a job description.", "", "", ""

    resume_text = extract_resume_text(pdf_file)

    if not resume_text.strip():
        return "Could not extract text. Please use a text-based PDF.", "", "", ""

    found_skills = []

    for skill in skills_list:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, resume_text, re.IGNORECASE):
            found_skills.append(skill)

    matched = []
    missing = []

    for skill in skills_list:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, job_description, re.IGNORECASE):
            if skill in found_skills:
                matched.append(skill)
            else:
                missing.append(skill)

    required_count = len(matched) + len(missing)

    score = (
        len(matched) / required_count * 100
        if required_count > 0 else 0
    )

    suggestions = []

    if missing:
        suggestions.append(
            "Consider developing these skills: " +
            ", ".join(missing)
        )

    if not found_skills:
        suggestions.append(
            "Add relevant technical and professional skills."
        )

    if not suggestions:
        suggestions.append(
            "Your listed skills match all detected job requirements."
        )

    report = f"""
    RESUME ANALYSIS REPORT

    Matching Score: {score:.2f}%

    Total Skills Found: {len(found_skills)}

    Matched Skills: {len(matched)}

    Missing Skills: {len(missing)}
    """

    return (
        report,
        ", ".join(found_skills) or "No skills detected",
        ", ".join(matched) or "No matched skills",
        "\n".join(suggestions)
    )

with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("# AI Resume Analyzer")
    gr.Markdown(
        "Upload your resume and compare your skills "
        "with your desired job requirements."
    )

    with gr.Row():

        resume = gr.File(
            label="Upload Your Resume (PDF)",
            file_types=[".pdf"],
            type="filepath"
        )

        job = gr.Textbox(
            label="Enter Job Description",
            placeholder="Example: Python, SQL, Machine Learning...",
            lines=8
        )

    analyze = gr.Button(
        "Analyze My Resume",
        variant="primary"
    )

    score = gr.Textbox(
        label="Resume Analysis Report"
    )

    with gr.Row():
        skills = gr.Textbox(
            label="Skills Found"
        )

        matched = gr.Textbox(
            label="Matched Skills"
        )

    suggestions = gr.Textbox(
        label="Improvement Suggestions",
        lines=4
    )

    analyze.click(
        fn=analyze_resume,
        inputs=[resume, job],
        outputs=[
            score,
            skills,
            matched,
            suggestions
        ]
    )

demo.launch(share=True)

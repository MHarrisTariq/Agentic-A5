import csv
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Tuple

JOB_DIR = Path("input_jobs")
RESUME_DIR = Path("input_resumes")
KB_DIR = Path("input_kb")
OUTPUT_DIR = Path("outputs")
TRACKER_DIR = Path("tracker")

KEYWORDS = [
    "python",
    "machine learning",
    "data preprocessing",
    "github",
    "git",
    "api",
    "prompt engineering",
    "sql",
    "communication",
    "problem solving",
    "oop",
    "database",
    "jupyter",
    "pandas",
    "numpy",
    "deep learning",
    "html",
    "css",
    "flask",
    "streamlit",
    "resume",
    "interview",
]


def ensure_folders() -> None:
    for folder in [JOB_DIR, RESUME_DIR, KB_DIR, OUTPUT_DIR, TRACKER_DIR, Path("samples")]:
        folder.mkdir(parents=True, exist_ok=True)


def read_file_content(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")

    if suffix == ".pdf":
        try:
            from pypdf import PdfReader  # type: ignore

            reader = PdfReader(str(path))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            return ""

    if suffix == ".docx":
        try:
            import docx  # type: ignore

            document = docx.Document(str(path))
            return "\n".join(paragraph.text for paragraph in document.paragraphs)
        except Exception:
            return ""

    return ""


def read_supported_files(folder: Path) -> Tuple[str, int]:
    combined_text: List[str] = []
    file_count = 0
    for path in sorted(folder.glob("*")):
        if path.suffix.lower() not in {".txt", ".pdf", ".docx"}:
            continue
        content = read_file_content(path).strip()
        if not content:
            continue
        combined_text.append(f"--- FILE: {path.name} ---\n{content}")
        file_count += 1
    return "\n\n".join(combined_text), file_count


def save_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def save_pdf_report(path: Path, title: str, sections: List[Tuple[str, str]]) -> bool:
    """
    Create a clean black-only PDF report.
    Returns True if PDF is created successfully, otherwise False.
    """
    try:
        from reportlab.lib import colors  # type: ignore
        from reportlab.lib.pagesizes import A4  # type: ignore
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # type: ignore
        from reportlab.lib.units import mm  # type: ignore
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer  # type: ignore

        document = SimpleDocTemplate(
            str(path),
            pagesize=A4,
            leftMargin=20 * mm,
            rightMargin=20 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name="BlackTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            textColor=colors.black,
            fontSize=16,
            spaceAfter=10,
        )
        heading_style = ParagraphStyle(
            name="BlackHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            textColor=colors.black,
            fontSize=12,
            spaceBefore=10,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            name="BlackBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            textColor=colors.black,
            fontSize=10,
            leading=14,
        )

        story = [Paragraph(title, title_style), Spacer(1, 6)]
        for section_title, content in sections:
            story.append(Paragraph(section_title, heading_style))
            for line in content.splitlines():
                if not line.strip():
                    story.append(Spacer(1, 4))
                    continue
                safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                story.append(Paragraph(safe_line, body_style))

        document.build(story)
        return True
    except Exception:
        return False


def extract_keywords(text: str) -> List[str]:
    text_lower = text.lower()
    return [keyword for keyword in KEYWORDS if keyword in text_lower]


def keyword_frequency(text: str, items: List[str]) -> Dict[str, int]:
    text_lower = text.lower()
    return {item: text_lower.count(item.lower()) for item in items}


def compare_skills(job_skills: List[str], resume_skills: List[str]) -> Tuple[List[str], List[str], float]:
    matched = [skill for skill in job_skills if skill in resume_skills]
    missing = [skill for skill in job_skills if skill not in resume_skills]
    score = 0.0 if not job_skills else round((len(matched) / len(job_skills)) * 100, 2)
    return matched, missing, score


def generate_job_analysis(job_text: str, job_skills: List[str]) -> str:
    frequencies = keyword_frequency(job_text, job_skills)
    report = ["Job Analysis Report", "===================", ""]
    if not job_skills:
        report.append("No tracked keywords were found in job posters.")
        return "\n".join(report)

    report.append("Skills/keywords found in job posters:")
    for skill in job_skills:
        report.append(f"- {skill} (mentions: {frequencies.get(skill, 0)})")
    return "\n".join(report)


def generate_skill_gap_report(
    job_skills: List[str], resume_skills: List[str], matched: List[str], missing: List[str], score: float
) -> str:
    report = [
        "Skill Gap Report",
        "================",
        "",
        f"Match Score: {score}%",
        "",
        f"Total job keywords: {len(job_skills)}",
        f"Total resume keywords: {len(resume_skills)}",
        "",
        "Matched Skills:",
    ]
    report.extend([f"- {skill}" for skill in matched] or ["- None"])
    report.append("")
    report.append("Missing Skills:")
    report.extend([f"- {skill}" for skill in missing] or ["- None"])
    return "\n".join(report)


def generate_resume_suggestions(job_skills: List[str], missing: List[str]) -> str:
    output = [
        "Tailored Resume Suggestions",
        "===========================",
        "",
        "Suggested improvements according to job posters:",
    ]
    for skill in job_skills:
        output.append(f"- Add measurable evidence (tools, outcome, impact) for {skill}.")

    output.extend(
        [
            "",
            "Suggested resume bullets:",
            "- Built Python-based projects and documented approach/results clearly.",
            "- Used Git/GitHub for version control, issue tracking, and collaboration.",
            "- Applied structured problem-solving in coursework and practical projects.",
        ]
    )

    if missing:
        output.extend(["", "Skills to improve before applying/interview:"])
        output.extend([f"- {skill}" for skill in missing])
    return "\n".join(output)


def generate_interview_questions(job_skills: List[str], kb_text: str) -> str:
    questions = ["Interview Questions", "===================", ""]
    questions.append("Technical questions based on job posters:")
    for skill in job_skills:
        questions.append(f"- Explain your understanding of {skill}.")
        questions.append(f"- Describe one project where you used {skill}.")

    questions.extend(
        [
            "",
            "HR and behavioral questions:",
            "- Tell me about yourself.",
            "- Why are you interested in this role?",
            "- Describe a challenge and how you solved it.",
            "- What are your strengths and areas for improvement?",
        ]
    )

    kb_lines = [line.strip("- ").strip() for line in kb_text.splitlines() if line.strip()]
    questions.extend(["", "Questions inspired by KB/slides:"])
    for line in kb_lines[:10]:
        questions.append(f"- How would you explain this point in an interview: {line}?")
    return "\n".join(questions)


def create_or_update_tracker() -> Path:
    path = TRACKER_DIR / "applications.csv"
    if path.exists():
        return path

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "application_id",
                "company",
                "role",
                "source",
                "status",
                "applied_date",
                "interview_date",
                "follow_up_date",
                "next_action",
                "notes",
            ]
        )
        writer.writerow(
            [
                "APP-001",
                "ABC Tech",
                "Junior AI Engineer Intern",
                "LinkedIn",
                "Interview Scheduled",
                str(date.today()),
                str(date.today().replace(day=min(date.today().day + 3, 28))),
                str(date.today().replace(day=min(date.today().day + 6, 28))),
                "Revise Python, ML basics, and explain projects clearly.",
                "Resume tailored and submitted.",
            ]
        )
        writer.writerow(
            [
                "APP-002",
                "DataWorks",
                "Data Analyst Intern",
                "Rozee",
                "Applied",
                str(date.today()),
                "",
                str(date.today().replace(day=min(date.today().day + 5, 28))),
                "Prepare SQL and dashboard case study.",
                "Waiting for response.",
            ]
        )
    return path


def generate_reminders() -> str:
    tracker_path = TRACKER_DIR / "applications.csv"
    reminders = ["Application Reminders", "=====================", ""]
    if not tracker_path.exists():
        return "No tracker file found."

    with tracker_path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            app_id = row.get("application_id", "")
            company = row.get("company", "")
            role = row.get("role", "")
            status = row.get("status", "").strip().lower()
            interview_date = row.get("interview_date", "").strip()
            follow_up_date = row.get("follow_up_date", "").strip()
            next_action = row.get("next_action", "").strip()

            if status == "interview scheduled":
                reminders.append(
                    f"- {app_id}: Interview scheduled for {role} at {company} on {interview_date}. Next action: {next_action}"
                )
            elif status == "not applied":
                reminders.append(
                    f"- {app_id}: Not applied yet for {role} at {company}. Tailor resume and apply."
                )
            elif status == "applied":
                reminders.append(
                    f"- {app_id}: Application submitted to {company}. Follow up on {follow_up_date} if no response."
                )

            if follow_up_date:
                reminders.append(f"- {app_id}: Follow-up date set to {follow_up_date}.")
    return "\n".join(reminders)


def generate_preparation_plan(missing: List[str], matched: List[str]) -> str:
    plan = [
        "Preparation Plan",
        "================",
        "",
        "Day 1-2: Strengthen missing skills",
    ]
    plan.extend([f"- Study and practice: {skill}" for skill in missing] or ["- No major missing skills detected."])
    plan.extend(["", "Day 3: Review your demonstrated strengths"])
    plan.extend([f"- Prepare project examples for: {skill}" for skill in matched] or ["- Build one end-to-end mini project."])
    plan.extend(["", "Day 4: Mock interview", "- Practice technical + HR questions for 30-45 minutes."])
    return "\n".join(plan)


def write_summary_metadata(job_count: int, resume_count: int, kb_count: int, score: float) -> str:
    parts = [
        "CareerPrep Job-Hunting Agent Report",
        "====================================",
        f"Generated on: {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"Job files read: {job_count}",
        f"Resume files read: {resume_count}",
        f"KB files read: {kb_count}",
        f"Skill match score: {score}%",
    ]
    return "\n".join(parts)


def run_agent() -> None:
    ensure_folders()
    job_text, job_count = read_supported_files(JOB_DIR)
    resume_text, resume_count = read_supported_files(RESUME_DIR)
    kb_text, kb_count = read_supported_files(KB_DIR)

    if job_count == 0 or resume_count == 0 or kb_count == 0:
        print("Please add supported files in input_jobs, input_resumes, and input_kb folders.")
        print("Supported formats: .txt (required for basic), .pdf/.docx (optional).")
        return

    job_skills = extract_keywords(job_text)
    resume_skills = extract_keywords(resume_text)
    matched, missing, score = compare_skills(job_skills, resume_skills)

    job_report = generate_job_analysis(job_text, job_skills)
    gap_report = generate_skill_gap_report(job_skills, resume_skills, matched, missing, score)
    resume_suggestions = generate_resume_suggestions(job_skills, missing)
    interview_questions = generate_interview_questions(job_skills, kb_text)
    preparation_plan = generate_preparation_plan(missing, matched)

    create_or_update_tracker()
    reminders = generate_reminders()
    summary = write_summary_metadata(job_count, resume_count, kb_count, score)

    final_report = "\n\n".join(
        [summary, job_report, gap_report, resume_suggestions, interview_questions, preparation_plan, reminders]
    )

    save_text(OUTPUT_DIR / "job_analysis_report.txt", job_report)
    save_text(OUTPUT_DIR / "skill_gap_report.txt", gap_report)
    save_text(OUTPUT_DIR / "tailored_resume_suggestions.txt", resume_suggestions)
    save_text(OUTPUT_DIR / "interview_questions.txt", interview_questions)
    save_text(OUTPUT_DIR / "preparation_plan.txt", preparation_plan)
    save_text(OUTPUT_DIR / "final_agent_report.txt", final_report)
    save_text(TRACKER_DIR / "reminders.txt", reminders)
    pdf_created = save_pdf_report(
        OUTPUT_DIR / "final_agent_report.pdf",
        "CareerPrep Job-Hunting Agent Report",
        [
            ("Run Summary", summary),
            ("Job Analysis", job_report),
            ("Skill Gap", gap_report),
            ("Tailored Resume Suggestions", resume_suggestions),
            ("Interview Questions", interview_questions),
            ("Preparation Plan", preparation_plan),
            ("Reminders", reminders),
        ],
    )

    print("Agent completed successfully.")
    print(f"Job files read: {job_count}")
    print(f"Resume files read: {resume_count}")
    print(f"KB files read: {kb_count}")
    print(f"Match score: {score}%")
    if pdf_created:
        print("PDF report generated: outputs/final_agent_report.pdf")
    else:
        print("PDF report skipped (install reportlab: pip install reportlab).")
    print("Outputs saved in outputs/ and tracker/ folders.")


if __name__ == "__main__":
    run_agent()

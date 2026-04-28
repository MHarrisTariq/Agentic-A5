# CareerPrep Job-Hunting Agent

This project is a file-driven Python agent for job-hunting workflow automation.  
It reads job posters, resume files, and knowledge-base notes from folders, then generates:

- Job analysis
- Skill-gap report
- Tailored resume suggestions
- Interview questions from KB
- Application tracker reminders
- Final black-only PDF report

## Repository Structure

- `app.py`
- `requirements.txt`
- `reflection.md`
- `input_jobs/`
- `input_resumes/`
- `input_kb/`
- `outputs/`
- `tracker/`
- `samples/`

## How to Run

1. Put at least one file in each folder:
   - `input_jobs/`
   - `input_resumes/`
   - `input_kb/`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run:
   - `python app.py`
4. Check generated files in:
   - `outputs/`
   - `tracker/`

## Supported Input Formats

- Basic (required): `.txt`
- Optional (extra): `.pdf`, `.docx`  
  (`.pdf` and `.docx` are only used if related libraries are available)

## Output Files

- `outputs/job_analysis_report.txt`
- `outputs/skill_gap_report.txt`
- `outputs/tailored_resume_suggestions.txt`
- `outputs/interview_questions.txt`
- `outputs/preparation_plan.txt`
- `outputs/final_agent_report.txt`
- `outputs/final_agent_report.pdf`
- `tracker/applications.csv`
- `tracker/reminders.txt`

## Unique/Extra Features Added

- Optional PDF and DOCX reading support.
- Preparation plan generation (`preparation_plan.txt`).
- Keyword mention counting in job analysis.
- Final black-only PDF report generation.
- Consolidated final report with run metadata.

# Reflection - File-Driven Job-Hunting Agent

## What I Built

I built a folder-based Python agent that reads:
- job posters from `input_jobs/`
- resume files from `input_resumes/`
- interview/course knowledge notes from `input_kb/`

The agent extracts tracked keywords, compares job requirements with resume skills, and generates reports in `outputs/`.  
It also creates/updates an application tracker in `tracker/applications.csv` and writes reminders to `tracker/reminders.txt`.

## What Was Tested

- Folder creation and file loading from required input directories.
- Keyword extraction from job and resume files.
- Skill matching with score, matched skills, and missing skills.
- Tailored resume suggestion generation.
- Interview question generation using KB content.
- Tracker initialization and reminder generation.
- Final output report generation in the required output files.

## Improvements Added

- Optional `.pdf` and `.docx` reading support for extra flexibility.
- Preparation plan generation for short interview prep.
- More informative job analysis with keyword mention counts.
- Cleaner final report that includes run timestamp and file counts.

## Challenges and Learnings

- The biggest challenge was keeping the workflow simple while still practical.
- A file-driven design is easy to test and avoids hardcoded input.
- Small structured outputs (TXT + CSV) are enough for a useful first version.

## Next Steps

- Add menu selection for choosing a specific job/resume pair.
- Add urgency logic (today/tomorrow/overdue) for reminders.
- Add cover letter and recruiter outreach message generation.

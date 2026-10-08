# AI Resume Screener

An AI-powered resume screening and ranking system that analyzes multiple resumes against a selected job role and ranks candidates based on skills, experience, projects, education, and certifications.

## Overview

The AI Resume Screener combines semantic role matching, Transformer-based resume understanding, exact skill verification, and career-stage-aware scoring to evaluate candidates.

The system accepts PDF and DOCX resumes, extracts relevant information, identifies skills, matches candidates to the selected job role, calculates an overall score, and ranks multiple candidates.

## Key Features

- Upload multiple PDF/DOCX resumes
- Natural-language job role input
- Semantic job-role matching using MiniLM
- Resume skill/entity extraction using a fine-tuned DistilBERT Resume-NER model
- Exact skill verification from resume text
- Required-skill matching with importance-based weighting
- Career-stage-aware scoring
- Candidate ranking
- Matched and missing skill identification
- Candidate comparison
- CSV export of ranking results
- Streamlit-based web interface

## System Architecture

```text
User Job Role
      ↓
MiniLM Semantic Role Matching
      ↓
Best Matching Role
      ↓
Required Skills
      ↓
Resume PDF / DOCX
      ↓
Text Extraction & Cleaning
      ↓
Resume-NER Transformer
      ↓
Detected Skills / Entities
      +
Exact Skill Verification
      ↓
Matched / Missing Skills
      ↓
Career-Stage-Aware Scoring
      ↓
Overall Candidate Score
      ↓
Candidate Ranking
      ↓
Streamlit Interface

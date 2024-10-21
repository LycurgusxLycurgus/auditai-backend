# Document Processing and Analysis System

## Overview

This application is a sophisticated document processing and analysis system designed to manage contracts (`contratos`), contract modifications (`otrosi`), and insurance policies (`poliza`). It automates the ingestion, indexing, information extraction, validation, discrepancy detection, and reporting of these documents.

## Technologies Used

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL (Supabase)
- **ORM:** SQLAlchemy
- **Asynchronous Task Queue:** Celery
- **OCR:** pytesseract
- **Excel Export:** openpyxl
- **Testing:** pytest, pytest-asyncio
- **Migrations:** Alembic


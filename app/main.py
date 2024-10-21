# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, engine
from app.models import Base
from app.queries import get_json_final
from app.templates.excel_export import create_excel_report
import os

app = FastAPI(title="Document Processing API")


@app.on_event("startup")
async def startup():
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/export/{consecutivo_contrato}", summary="Export contract data to Excel")
async def export_contract(consecutivo_contrato: str, db: AsyncSession = Depends(get_db)):
    json_data = await get_json_final(consecutivo_contrato, db)
    if not json_data:
        raise HTTPException(status_code=404, detail="Contract not found or already processed.")

    output_filename = f"{consecutivo_contrato}_report.xlsx"
    output_path = os.path.join("reports", output_filename)

    os.makedirs("reports", exist_ok=True)
    create_excel_report(json_data, output_path)

    return {"message": "Excel report generated successfully.", "file_path": output_path}

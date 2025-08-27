from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from celery.result import AsyncResult
import os
import uuid
from database import init_db, get_result
from celery_worker import run_analysis_crew

app = FastAPI(title="Financial Document Analyzer Pro")

@app.on_event("startup")
def on_startup():
    """Initialize the database on application startup."""
    init_db()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_financial_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """
    Accepts a financial document, saves it, and queues it for analysis.
    Returns a task ID for retrieving the result later.
    """
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        if not query:
            query = "Analyze this financial document for investment insights"
            
        # Send the analysis task to the Celery worker
        task = run_analysis_crew.delay(query=query.strip(), file_path=file_path)
        
        return {"task_id": task.id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error queuing analysis task: {str(e)}")

@app.get("/results/{task_id}")
async def get_analysis_result(task_id: str):
    """
    Retrieves the result of a financial analysis task using its ID.
    First checks the database, then falls back to the Celery backend.
    """
    # Check our database first
    db_result = get_result(task_id)
    if db_result:
        return {
            "task_id": task_id,
            "status": db_result["status"],
            "result": db_result["result"]
        }

    # Fallback to Celery backend if not in DB (e.g., still processing)
    task_result = AsyncResult(task_id, app=run_analysis_crew.app)
    
    if task_result.state == 'PENDING':
        return {"task_id": task_id, "status": "PENDING"}
    elif task_result.state == 'FAILURE':
        return {"task_id": task_id, "status": "FAILURE", "result": str(task_result.info)}
    
    return {"task_id": task_id, "status": task_result.state, "result": task_result.result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
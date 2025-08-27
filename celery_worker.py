import os
from celery import Celery
from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analysis_task, verification_task, investment_task, risk_assessment_task
from database import init_db, save_result

# Initialize the database
init_db()

# Configure Celery
celery = Celery(
    "financial_analyzer",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.update(
    task_track_started=True,
)

@celery.task(name="run_analysis_crew")
def run_analysis_crew(query: str, file_path: str):
    """Celery task to run the financial analysis crew."""
    task_id = run_analysis_crew.request.id
    save_result(task_id, status="STARTED")

    try:
        financial_crew = Crew(
            agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
            tasks=[verification_task, analysis_task, investment_task, risk_assessment_task],
            process=Process.sequential,
            verbose=2
        )
        
        result = financial_crew.kickoff({'query': query, 'file_path': file_path})
        
        save_result(task_id, status="SUCCESS", result=str(result))
        return str(result)
    
    except Exception as e:
        save_result(task_id, status="FAILURE", result=str(e))
        return str(e)
    
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error cleaning up file in worker: {e}")
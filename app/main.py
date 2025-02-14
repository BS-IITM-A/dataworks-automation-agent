from fastapi import FastAPI, Query, Body, HTTPException
from typing import Optional
import logging

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.post("/run")
def run_task(
    task: Optional[str] = Query(None, description="Task description from query parameter"),
    body: Optional[dict] = Body(None)
):
    """Accepts a task as a query parameter or JSON body and processes it."""
    
    # Get task value from query param or JSON body
    task_value = task or (body.get("task") if body else None)

    if not task_value:
        logging.error("Task is missing in request")
        raise HTTPException(status_code=400, detail="Task is required! Use ?task=... or {'task': '...'} in JSON.")

    logging.info(f"Processing task: {task_value}")
    
    # Placeholder for actual task processing logic
    return {"task_received": task_value}

@app.get("/read")
def read_file(path: str = Query(..., description="Path of the file to read")):
    """Reads a file from the specified path and returns its content."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        return {"content": content}
    except FileNotFoundError:
        logging.error(f"File not found: {path}")
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/")
def root():
    """Root endpoint for health check."""
    return {"message": "DataWorks Automation Agent API is running!"}

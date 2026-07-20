from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel

app=FastAPI()

class Task(BaseModel):
    id:int
    title:str
    done:bool = False
    
    
tasks=[Task(id=1, title="Learn FastAPI", done=False),
       Task(id=2, title="Build a REST API", done=False),
       Task(id=3, title="Deploy the API", done=False)]

@app.get("/")
def root():
    return {"name":"Task API" ,"version":"1.0","endpoints":["/tasks","/health"]}


@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_task(title:str):
    if not title.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Title is required and cannot be empty")
    else:
        tasks.append(Task(id=len(tasks)+1, title=title.strip(), done=False))
        
        return tasks[-1]
        
         
@app.get("/tasks")
def get_task():
    return tasks


@app.get("/tasks/{id}")
def get_task(id:int):
    for task in tasks:
        if task.id == id:
            return task
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Task {id} not found")


@app.put("/tasks/{id}")
def update_task(id:int,title:str=None,done:bool=None):
    
    if title is None and done is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="At least one field (title or done) must be provided for update")
    
    if title is not None and not title.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Title can't be empty")
    
    for task in tasks:
        if task.id==id:
            if title is not None:
                task.title=title
            if done is not None:
                task.done=done
            return task
        
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Task {id} not found")


@app.delete("/tasks/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id:int):    
    for task in tasks:
        if task.id==id:
            tasks.remove(task)
            return {}
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": f"Task {id} not found"}
    )
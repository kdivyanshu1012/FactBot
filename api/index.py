
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from checker import check_fact

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/check", response_class=HTMLResponse)
async def check(request: Request, fact: str = Form(...)):
    result = check_fact(fact)
    return templates.TemplateResponse("index.html", {"request": request, "fact": fact, "result": result})

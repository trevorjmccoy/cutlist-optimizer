from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from optimizer import best_fit

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit-form")
async def run_optimizer(
    request: Request,
    depth: float = Form(),
    stocks_lengths: List[float] = Form(...),
    stocks_quantities: List[int] = Form(...),
    cuts_lengths: List[float] = Form(...),
    cuts_quantities: List[int] = Form(...),
    cuts_left_wall_angles: List[str] = Form(...),
    cuts_right_wall_angles: List[str] = Form(...)
):  
    # Replace empty values with 180 while keeping valid numbers
    cuts_left_wall_angles = [float(angle) if angle.strip() else 180 for angle in cuts_left_wall_angles]
    cuts_right_wall_angles = [float(angle) if angle.strip() else 180 for angle in cuts_right_wall_angles]

    # Sort cuts into stocks leaving as little spare as possible
    return best_fit(
        depth, 
        stocks_lengths, 
        stocks_quantities, 
        cuts_lengths, 
        cuts_quantities, 
        cuts_left_wall_angles, 
        cuts_right_wall_angles
    )

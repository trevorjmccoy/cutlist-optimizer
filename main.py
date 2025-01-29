from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit-form")
async def run_optimizer(
    request: Request,
    stock_lengths: List[float] = Form(...),
    stock_quantities: List[int] = Form(...),
    cut_lengths: List[float] = Form(...),
    cut_quantities: List[int] = Form(...),
):
    form_data = await request.form()
    
    # Extract cut_plus_values with unique names
    cut_plus_values = [
        int(value) for key, value in form_data.items() if key.startswith("cut_plus_values_")
    ]

    return JSONResponse({
        "stock_lengths": stock_lengths,
        "stock_quantities": stock_quantities,
        "cut_lengths": cut_lengths,
        "cut_quantities": cut_quantities,
        "cut_plus_values": cut_plus_values
    })
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from optimizer import first_fit, best_fit

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mock data to store table rows
rows = [{"length": "", "width": "", "quantity": ""}]

stocks = [""]
cuts = [""]

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "rows": rows, "stocks": stocks, "cuts": cuts})


@app.post("/update_tables")
async def update_tables(
    action: str = Form(...),
    stock_lengths: list[str] = Form(default_factory=list),
    cut_lengths: list[str] = Form(default_factory=list),
    cut_quantities: list[str] = Form(default_factory=list)
):
    global stocks, cuts

    # Update stocks
    stocks = stock_lengths or []

    # Update cuts
    cuts = [{"length": l, "quantity": q} for l, q in zip(cut_lengths, cut_quantities)]

    # Handle actions
    if action == "add_stock":
        stocks.append("")
    elif action.startswith("delete_stock_"):
        index = int(action.split("_")[2])
        if 0 <= index < len(stocks):
            stocks.pop(index)

    if action == "add_cut":
        cuts.append({"length": "", "quantity": ""})
    elif action.startswith("delete_cut_"):
        index = int(action.split("_")[2])
        if 0 <= index < len(cuts):
            cuts.pop(index)

    # Return updated page
    return templates.TemplateResponse("index.html", {"request": {}, "stocks": stocks, "cuts": cuts})






@app.post("/run_best_fit")
async def run_best_fit():
    # Implement your best fit algorithm using `stocks` and `cuts`
    # optimized_layout = best_fit_algorithm(stocks, cuts)
    # Store or display the result
    # return 
    pass
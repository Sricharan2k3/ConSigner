import google.generativeai as genai
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Form, Request
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List, Tuple
from fastapi.middleware.cors import CORSMiddleware
# Import your solve_routing_problem function from another file
from last_mile import solve_routing_problem
from runMCTS import runMCTS
import json

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class Order(BaseModel):
    names: List[str]
    locations: List[Tuple[float, float]]
    demands: List[int]
    capacities: List[int]
    vehicles: int


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/solve-routing-problem")
async def solve_routing_problem_endpoint(orders: Order):
    if orders is None:
        raise HTTPException(
            status_code=400, detail="Missing 'order' query parameter")
    # Process the request with the provided 'order' parameter
    # return {"message": f"Received order: {orders}"}
    coordinates = orders.locations
    demands = orders.demands
    vehicle_capacities = orders.capacities
    num_vehicles = orders.vehicles

    results = solve_routing_problem(
        coordinates, demands, vehicle_capacities, num_vehicles)
    if results is not None:
        data = []
        for i, result in enumerate(results):
            data.append({
                'driver': i,
                'route': result['route'],
                'total_distance': result['total_distance'],
                'parcels_delivered': result['parcels_delivered']
            })

        return data
    else:
        raise HTTPException(status_code=404, detail="No Solution")


@app.post("/package-optimize")
def package_optimize():
    runMCTS()


# package_optimize()


@app.post("/description")
def extract_dimensions(description):
    genai.configure(api_key='AIzaSyBzVKMG7njlSoQCcZeKSTGm73uX36iSdnM')
    model = genai.GenerativeModel('gemini-pro')
    resp = model.generate_content("Please estimate the product type based on the following description: " + description +
                                  ". Provide the average dimensions (length, width, and height) of similar products in millimeters. ")

    print(resp.text)

    # Define regular expressions to extract dimensions
    length_pattern = r"Length:\s*(\d+)\s*mm"
    width_pattern = r"Width:\s*(\d+)\s*mm"
    height_pattern = r"Height:\s*(\d+)\s*mm"

    # Search for dimensions in the output text
    length_match = re.search(length_pattern, resp.text)
    width_match = re.search(width_pattern, resp.text)
    height_match = re.search(height_pattern, resp.text)

    # Extract dimensions if found
    length = int(length_match.group(1)) if length_match else None
    width = int(width_match.group(1)) if width_match else None
    height = int(height_match.group(1)) if height_match else None

    print("Length:", length)
    print("Width:", width)
    print("Height:", height)

    return length, width, height


extract_dimensions("Blue Star 1.5 Ton 3 Star Inverter Split AC (Copper, Smart Ready, 5 in 1 Convertible, Turbo Cool, ID318YKU, 2023 Model, White), About this item Turbo Cool: Pre-set mode to instantly cool the room during extreme summers.  5-in-1 Convertible Cooling: Unique 5-in-1 cooling mode to run your AC at 5 different capacities as per the desired comfort. It comes in combination of 2 buttons in the remote. Smart Ready: The AC is ready to be operated* using Blue Star's Smart App and through Voice Command using Amazon Alexa or Google Home *To operate through Smart App or Voice Command, user has to pay an additional charge to convert the AC into Smart AC completely. Manufacturer Warranty : 10 years warranty on inverter compressor, 5 years on PCB and 1 Year Warranty on Product (*T&C) Energy Saver: The Eco mode helps save on your electricity bills, while giving you comfortable cooling experience.")

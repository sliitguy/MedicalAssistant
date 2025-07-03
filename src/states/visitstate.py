from typing import TypedDict
from pydantic import BaseModel, Field


class Patient(BaseModel):
    name:str=Field(description="The name of the patient")
    insurance:str=Field(description="The name of the insurance")
    age:int=Field(description="The age of the patient")

class VisitState(TypedDict):
    patient_data: dict
    diagnosis: str
    notes: str

class Visit(BaseModel):
    start_time: str=Field(description="The start time of the patient visit")
    end_time: str=Field(description="The end time of the patient visit")
    chief_complaint: str=Field(description="The chief complaint for the visit")
    visit_type: str=Field(description="The visit type")


class Note(BaseModel):
    content:str=Field(description="The main content of the medical note")
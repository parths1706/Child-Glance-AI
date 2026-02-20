from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# --- Base Models ---

class ChildDetails(BaseModel):
    dob: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    tob: Optional[str] = Field("12:00 PM", description="Time of birth (e.g., '10:30 AM')")
    city: str = Field(..., description="City of birth")
    country: str = Field(..., description="Country of birth")
    name: Optional[str] = Field("Child", description="Child's name")
    
    # Computed fields for internal logic, optionally passed if pre-calculated
    age_years: Optional[int] = None
    age_months: Optional[int] = None


# --- Astrology Service ---

class AstrologyRequest(BaseModel):
    child_details: ChildDetails

class AstrologyOutput(BaseModel):
    sun_sign: str = Field(..., description="Sun Sign in 'Hindi Name (English Name)' format")
    moon_sign: str = Field(..., description="Moon Sign in 'Hindi Name (English Name)' format")


# --- Insights Service ---

class InsightsRequest(BaseModel):
    child_details: ChildDetails
    astrology_output: AstrologyOutput

class Trait(BaseModel):
    trait: str
    description: str

class Need(BaseModel):
    need: str
    description: str

class Strength(BaseModel):
    strength: str
    description: str

class Area(BaseModel):
    area: str
    description: str

class InsightsOutput(BaseModel):
    core_personality: List[Trait]
    emotional_needs: List[Need]
    strengths: List[Strength]
    growth_areas: List[Area]


# --- Parenting Tips Service ---

class TipsRequest(BaseModel):
    child_details: ChildDetails
    insights_output: InsightsOutput

class TipsOutput(BaseModel):
    responsibility: str
    appreciation: str
    balance_advice: str


# --- Daily Tasks Service ---

class TasksRequest(BaseModel):
    child_details: ChildDetails
    tips_output: TipsOutput

class TaskItem(BaseModel):
    type: str = Field(..., description="Type of task (e.g., Discipline Task)")
    title: str
    description: str
    todo_task: str
    reward_stars: int = Field(..., description="Stars earned for completing the task (10-200)")

class TasksOutput(BaseModel):
    daily_tasks: List[TaskItem]


# --- Orchestrator ---

class FullReportResponse(BaseModel):
    astrology: AstrologyOutput
    insights: InsightsOutput
    parenting_tips: TipsOutput
    daily_tasks: TasksOutput

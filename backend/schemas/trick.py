from typing import Optional
from pydantic import BaseModel, Field

class Trick(BaseModel):
    name: str = Field(..., description="Name of the trick")
    difficulty: int = Field(..., description="Difficulty can be the humber from 1 to 10")
    video_link: Optional[str] = Field(None, description="The tutuiral video of the trick")
    tips: Optional[str] = Field(None, description="The text description of the trick tips")

class TrickUpdate(Trick):
    new_name: Optional[str] = Field(..., description="Name of the trick")
    difficulty: Optional[int] = Field(None, description="Difficulty can be the humber from 1 to 10")
    video_link: Optional[str] = Field(None, description="The tutuiral video of the trick")
    tips: Optional[str] = Field(None, description="The text description of the trick tips")

class StudentTrick(BaseModel):
    trick_name: str = Field(..., description="Name of the trick")
    proficiency: int = Field(..., description="Number from 0 to 100, student can't change this, only by his/her teacher")
    remark: Optional[str] = Field(None, description="Teacher can leaves some remark here")

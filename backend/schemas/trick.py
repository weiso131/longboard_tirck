from typing import Optional
from pydantic import BaseModel, Field
from beanie import Document



class TrickBase(BaseModel):
    name: str = Field(..., description="Name of the trick")
    difficulty: int = Field(..., description="Difficulty can be the humber from 1 to 10")
    video_link: Optional[str] = Field(None, description="The tutuiral video of the trick")
    tips: Optional[str] = Field(None, description="The text description of the trick tips")

class Trick(TrickBase, Document):
    pass

class TrickUpdate(TrickBase):
    name: Optional[str] = Field(..., description="Name of the trick")
    difficulty: Optional[int] = Field(None, description="Difficulty can be the humber from 1 to 10")
    video_link: Optional[str] = Field(None, description="The tutuiral video of the trick")
    tips: Optional[str] = Field(None, description="The text description of the trick tips")

class StudentTrickBase(BaseModel):
    name: str = Field(..., description="Name of the trick")
    proficiency: int = Field(..., description="Number from 0 to 100, student can't change this, only by his/her teacher")
    remark: Optional[str] = Field(None, description="Teacher can leaves some remark here")

class StudentTrickCreate(StudentTrickBase):
    pass

class StudentTrickWithUid(StudentTrickBase):
    uid: str

class StudentTrick(StudentTrickWithUid, Document):
    pass


class StudentTrickUpdate(StudentTrickBase):
    name: Optional[str] = Field(None, description="Name of the trick")
    proficiency: Optional[int] = Field(None, description="Number from 0 to 100, student can't change this, only by his/her teacher")
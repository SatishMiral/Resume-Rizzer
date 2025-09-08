from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional

class BasicInfo(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr


class SocialLinks(BaseModel):
    github: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None
    portfolio: Optional[HttpUrl] = None
    leetcode: Optional[HttpUrl] = None
    gfg: Optional[HttpUrl] = None


class Skill(BaseModel):
    name: str
    proficiency: Optional[str] = None  


class Project(BaseModel):
    title: str
    description: str
    tech_stack: List[str]
    link: Optional[HttpUrl] = None


class Experience(BaseModel):
    company: str
    role: str
    start_date: str
    end_date: Optional[str] = None
    description: List[str]


class Education(BaseModel):
    institution: str
    degree: str
    field: str
    start_year: int
    end_year: int
    grade: Optional[str] = None


class Certificate(BaseModel):
    name: str
    issuer: str
    date: str
    link: Optional[HttpUrl] = None


class Achievement(BaseModel):
    title: str
    description: Optional[str] = None


class ExtraCurricular(BaseModel):
    activity: str
    description: Optional[str] = None


class ResumeData(BaseModel):
    basic_info: Optional[BasicInfo] = None
    social_links: Optional[SocialLinks] = None
    skills: Optional[List[Skill]] = None
    projects: Optional[List[Project]] = None
    experience: Optional[List[Experience]] = None
    education: Optional[List[Education]] = None
    certificates: Optional[List[Certificate]] = None
    achievements: Optional[List[Achievement]] = None
    extra_curricular: Optional[List[ExtraCurricular]] = None
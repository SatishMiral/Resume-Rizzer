from fastapi import APIRouter, Depends
from typing import List
from app.schemas.information import (
    BasicInfo, SocialLinks, Skill, Project, Education, Experience, ExtraCurricular, Certificate, Achievement, ResumeData
)
from app.core.security import get_current_user
from app.schemas import auth

router = APIRouter(prefix="/info", tags=["Information"])

# Full Resume Endpoints

@router.post("/")
def create_resume(
    data: ResumeData, 
    current_user: auth.UserLogin = Depends(get_current_user)
):
    """
    Create a new resume with all sections.
    Users can submit full resume data in one request.
    """
    return {"resume": data.model_dump()}


@router.patch("/")
def update_resume(
    data: ResumeData,
    current_user: auth.UserLogin = Depends(get_current_user)
):
    """
    Update the full resume. Any section not provided will remain unchanged.
    """
    return {"updated_resume": data.model_dump()}


# Section-Specific Endpoints

@router.patch("/basic")
def update_basic(
    info: BasicInfo,
    current_user: auth.UserLogin = Depends(get_current_user)
):
    """Update basic information of the resume."""
    return {"basic_info": info.model_dump()}


@router.patch("/social_links")
def update_socials(
    links: SocialLinks,
    current_user: auth.UserLogin = Depends(get_current_user)
):
    """Update social and professional links of the resume."""
    return {"social_links": links.model_dump()}


@router.patch("/skills")
def update_skills(
    skills: List[Skill],
    current_user: auth.UserLogin = Depends(get_current_user)
):
    """Update skills section of the resume."""
    return {"skills": [s.model_dump() for s in skills]}


@router.patch("/projects")
def update_projects(
    projects: List[Project],
    current_user: auth.UserLogin = Depends(get_current_user)
):
    """Update projects section of the resume."""
    return {"projects": [p.model_dump() for p in projects]}


@router.patch("/experience")
def update_experience(
    experiences: List[Experience],
    current_user: auth.UserLogin = Depends(get_current_user)
):
    """Update experience section of the resume."""
    return {"experience": [e.model_dump() for e in experiences]}


@router.patch("/education")
def update_education(
    education: List[Education],
    current_user: auth.UserLogin = Depends(get_current_user)
):
    """Update education section of the resume."""
    return {"education": [e.model_dump() for e in education]}


@router.patch("/certificates")
def update_certificates(
    certificates: List[Certificate],
    current_user: auth.UserLogin = Depends(get_current_user)
):
    """Update certifications section of the resume."""
    return {"certificates": [c.model_dump() for c in certificates]}


@router.patch("/achievements")
def update_achievements(
    achievements: List[Achievement],
    current_user: auth.UserLogin = Depends(get_current_user)
):
    """Update achievements section of the resume."""
    return {"achievements": [a.model_dump() for a in achievements]}


@router.patch("/extra_curricular")
def update_extra_curricular(
    activities: List[ExtraCurricular],
    current_user: auth.UserLogin = Depends(get_current_user)
):
    """Update extra-curricular activities section of the resume."""
    return {"extra_curricular": [act.model_dump() for act in activities]}
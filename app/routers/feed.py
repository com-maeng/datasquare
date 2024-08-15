import base64

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.models.database import Base, SessionLocal, engine
from app.models.issue import Issue, TeamProfile, TeamMembership

Base.metadata.create_all(bind=engine)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/feed")
async def read_dashboard(request: Request, db: Session = Depends(get_db)):
    # retrieve teams list
    teams = db.query(TeamProfile).with_entities(
        TeamProfile.team_name, TeamProfile.profile_id).all()

    issues = db.query(Issue).filter_by(is_private=0).all()

    issue_data = []

    for issue in issues:
        author = issue.publisher
        author_team_name = db.query(TeamMembership).filter_by(
            member_id=author.profile_id).first().team.team_name

        issue_data.append({
            "title": issue.title,
            "content": issue.content,
            "author_name": author.name,
            "team": author_team_name,
            "profile_pic": base64.b64encode(author.profile_image).decode("utf-8")
        })

    return templates.TemplateResponse("feed.html", {"request": request, "teams": teams, "issues": issue_data, "teams": teams})


@router.get("/feed/my_issues")
async def read_my_issues(request: Request, db: Session = Depends(get_db)):
    teams = db.query(TeamProfile).with_entities(
        TeamProfile.team_name, TeamProfile.profile_id).all()
    # 'author_id='에 로그인 유저 ID 값 입력 필요(예시 ID: 1)
    my_issues = db.query(Issue).filter_by(publisher_id=1).all()

    issue_data = []

    for issue in my_issues:
        author = issue.publisher
        author_team_name = db.query(TeamMembership).filter_by(
            member_id=author.profile_id).first().team.team_name

        issue_data.append({
            "title": issue.title,
            "content": issue.content,
            "author_name": author.name,
            "team": author_team_name,
            "profile_pic": base64.b64encode(author.profile_image).decode("utf-8")
        })

    return templates.TemplateResponse("feed.html", {"request": request, "teams": teams, "issues": issue_data})


@router.get("/feed/search")
async def search_issues(request: Request, keyword: str, db: Session = Depends(get_db)):
    teams = db.query(TeamProfile).with_entities(
        TeamProfile.team_name, TeamProfile.profile_id).all()
    search_result = db.query(Issue).filter(
        Issue.title.contains(keyword)).all()

    result_data = []

    for issue in search_result:
        author = issue.publisher
        author_team_name = db.query(TeamMembership).filter_by(
            member_id=author.profile_id).first().team.team_name

        result_data.append({
            "title": issue.title,
            "content": issue.content,
            "author_name": author.name,
            "team": author_team_name,
            "profile_pic": base64.b64encode(author.profile_image).decode("utf-8")
        })

    return templates.TemplateResponse("feed.html", {"request": request, "teams": teams, "issues": result_data})

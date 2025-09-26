from fastapi import APIRouter, Depends
from ..auth import get_current_user
from ..outlook_integration import call_graph_with_user_token
from .. import db as dbmod

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("/me")
def get_profile(current_user = Depends(get_current_user), db = Depends(dbmod.get_db)):
    data = {"username": current_user.username, "outlook_email": current_user.outlook_email}
    try:
        graph = call_graph_with_user_token(db, current_user)
        data["outlook_profile"] = graph
    except Exception:
        data["outlook_profile"] = None
    return data
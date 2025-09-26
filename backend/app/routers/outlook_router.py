from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.orm import Session
import uuid
import os
from .. import db as dbmod, models
from ..auth import get_current_user
from ..outlook_integration import get_auth_url, acquire_token_by_auth_code
from datetime import datetime

router = APIRouter(prefix="/api/outlook", tags=["outlook"])

@router.get("/login")
def outlook_login(request: Request, current_user=Depends(get_current_user), db: Session = Depends(dbmod.get_db)):
    # generate state and redirect to Microsoft login
    state = str(uuid.uuid4())
    # simple state storage: store mapping in memory or persistent store. Here we use a short cookie which the callback will verify
    redirect_uri = os.getenv("MSAL_REDIRECT_URI", "http://localhost:8000/api/outlook/callback")
    auth_url = get_auth_url(redirect_uri=redirect_uri, state=state)
    # set a state cookie for CSRF (short-lived)
    response = Response(status_code=302)
    response.headers["Location"] = auth_url
    response.set_cookie("msal_state", state, httponly=True, max_age=300)
    return response

@router.get("/callback")
def outlook_callback(request: Request, code: str = None, state: str = None, db: Session = Depends(dbmod.get_db)):
    # verify cookie state
    cookie_state = request.cookies.get("msal_state")
    if not cookie_state or cookie_state != state:
        raise HTTPException(status_code=400, detail="Invalid or missing state")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")
    redirect_uri = os.getenv("MSAL_REDIRECT_URI", "http://localhost:8000/api/outlook/callback")
    token_data = acquire_token_by_auth_code(code=code, redirect_uri=redirect_uri)
    # We still need to determine the current logged-in user: require a session or token param
    # For simplicity, expect the client to include a Bearer token in the callback request (if called directly).
    # In most flows, the frontend will call backend /api/outlook/login while authenticated and will receive redirect through browser with cookies (we use cookie_state only).
    # We'll associate the token to the currently authenticated user via Authorization header if present.
    auth_header = request.headers.get("Authorization")
    user = None
    if auth_header and auth_header.startswith("Bearer "):
        from ..auth import get_current_user as _get_current_user
        try:
            # get_current_user expects dependencies; here we decode token with same secret
            # we'll attempt to decode the token into username manually via jwt
            from jose import jwt
            from ..auth import SECRET_KEY, ALGORITHM
            payload = jwt.decode(auth_header.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                user = db.query(models.User).filter(models.User.username == username).first()
        except Exception:
            user = None
    if not user:
        # fallback: if cookie-based session not available, return tokens and instruct client to post them to an authenticated endpoint
        return {"detail": "Authorization header missing. Exchange completed; send tokens to /api/outlook/store-token while authenticated.", "token_data": {"expires_at": token_data["expires_at"].isoformat()}}
    # store tokens
    token = models.OutlookToken(user_id=user.id, access_token=token_data["access_token"], refresh_token=token_data.get("refresh_token"), expires_at=token_data["expires_at"])
    db.add(token)
    db.commit()
    return {"detail": "Outlook tokens saved for user."}
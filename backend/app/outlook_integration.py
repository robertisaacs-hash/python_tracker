"""
Server-side helpers to call Microsoft Graph using stored per-user tokens,
refresh tokens when expired, and to do an application-level fetch.

This file provides:
- build_msal_app_confidential()
- get_auth_url(state)
- acquire_token_by_auth_code(code)
- refresh_token_for_user(stateful token storage is in OutlookToken model)
- call_graph_with_user_token(db, user, endpoint)
"""

import os
import msal
import requests
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models

CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")
TENANT_ID = os.getenv("AZURE_TENANT_ID", "")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}" if TENANT_ID else None
if not CLIENT_ID or not CLIENT_SECRET or not TENANT_ID:
    # we don't hard-fail here to allow some functionality without Azure configured,
    # but log or raise in production if necessary
    pass
SCOPES = ["User.Read", "offline_access"]  # request refresh token
GRAPH_ME = "https://graph.microsoft.com/v1.0/me"

def build_msal_app_confidential():
    return msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY
    )

def get_auth_url(redirect_uri: str, state: str):
    app = build_msal_app_confidential()
    return app.get_authorization_request_url(scopes=SCOPES, state=state, redirect_uri=redirect_uri)

def acquire_token_by_auth_code(code: str, redirect_uri: str):
    app = build_msal_app_confidential()
    result = app.acquire_token_by_authorization_code(code=code, scopes=SCOPES, redirect_uri=redirect_uri)
    # result contains access_token, refresh_token, expires_in etc.
    if "access_token" in result:
        expires_at = datetime.utcnow() + timedelta(seconds=int(result.get("expires_in", 3600)))
        return {
            "access_token": result["access_token"],
            "refresh_token": result.get("refresh_token"),
            "expires_at": expires_at
        }
    raise Exception(result.get("error_description") or "Failed to acquire token")

def refresh_token(db: Session, outlook_token: models.OutlookToken):
    app = build_msal_app_confidential()
    result = app.acquire_token_by_refresh_token(refresh_token=outlook_token.refresh_token, scopes=SCOPES)
    if "access_token" in result:
        outlook_token.access_token = result["access_token"]
        outlook_token.refresh_token = result.get("refresh_token", outlook_token.refresh_token)
        outlook_token.expires_at = datetime.utcnow() + timedelta(seconds=int(result.get("expires_in", 3600)))
        db.add(outlook_token)
        db.commit()
        db.refresh(outlook_token)
        return outlook_token
    else:
        raise Exception(result.get("error_description") or "Failed to refresh token")

def call_graph_with_user_token(db: Session, user: models.User, endpoint=GRAPH_ME):
    # find token for user
    token = None
    if user.outlook_tokens:
        token = user.outlook_tokens[0]
    if not token:
        raise Exception("No Outlook token for user")
    # refresh if expired (with 60s slack)
    if token.expires_at and token.expires_at < datetime.utcnow() + timedelta(seconds=60):
        token = refresh_token(db, token)
    resp = requests.get(endpoint, headers={"Authorization": f"Bearer {token.access_token}"})
    resp.raise_for_status()
    return resp.json()
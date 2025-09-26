import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { Paper, Typography } from "@mui/material";

export default function ProfilePage(){
  const [profile, setProfile] = useState<any>(null);
  useEffect(()=>{ api.get("/profile/me").then(r=>setProfile(r.data)).catch(()=>setProfile(null)); }, []);
  return (
    <Paper sx={{p:2}}>
      <Typography variant="h6">Profile</Typography>
      <pre>{JSON.stringify(profile, null, 2)}</pre>
    </Paper>
  );
}
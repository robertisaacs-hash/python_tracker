import React, { useState } from "react";
import { Paper, TextField, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage(){
  const { login } = useAuth();
  const [username,setUsername] = useState("");
  const [password,setPassword] = useState("");
  const nav = useNavigate();

  const submit = async () => {
    try {
      await login(username, password);
      nav("/");
    } catch(e){
      alert("Login failed");
    }
  };

  return (
    <Paper sx={{p:4, maxWidth:400, mx:"auto"}}>
      <Typography variant="h5" gutterBottom>Login</Typography>
      <TextField label="Username" value={username} onChange={e=>setUsername(e.target.value)} fullWidth sx={{mb:2}}/>
      <TextField label="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} fullWidth sx={{mb:2}}/>
      <Button variant="contained" onClick={submit} fullWidth>Login</Button>
    </Paper>
  );
}
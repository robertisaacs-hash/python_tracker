import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";
import ProjectsPage from "./pages/Projects";
import ProfilePage from "./pages/Profile";
import { useAuth } from "./context/AuthContext";
import { Container } from "@mui/material";

export default function App() {
  const { token } = useAuth();
  return (
    <Container sx={{mt:4}}>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/profile" element={token ? <ProfilePage /> : <Navigate to="/login" />} />
        <Route path="/" element={token ? <ProjectsPage /> : <Navigate to="/login" />} />
      </Routes>
    </Container>
  );
}
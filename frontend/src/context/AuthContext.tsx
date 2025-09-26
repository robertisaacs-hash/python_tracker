import React, { createContext, useContext, useState, useEffect } from "react";
import api from "../api/axios";

type AuthContextType = {
  token: string | null;
  user: any | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username:string, password:string, outlook_email?: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType>({} as any);

export const AuthProvider: React.FC<{children:any}> = ({ children }) => {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem("token"));
  const [user, setUser] = useState<any | null>(null);

  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
      api.get("/profile/me").then(r => setUser(r.data)).catch(()=>setUser(null));
    } else {
      localStorage.removeItem("token");
      setUser(null);
    }
  }, [token]);

  const login = async (username:string, password:string) => {
    const form = new URLSearchParams();
    form.append("username", username);
    form.append("password", password);
    form.append("grant_type", "password");
    const res = await api.post("/auth/token", form);
    setToken(res.data.access_token);
  };

  const register = async (username:string, password:string, outlook_email?:string) => {
    await api.post("/auth/register", { username, password, outlook_email });
  };

  const logout = () => setToken(null);

  return <AuthContext.Provider value={{ token, user, login, register, logout }}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
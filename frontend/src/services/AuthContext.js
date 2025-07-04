import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const data = localStorage.getItem('user');
    return data ? JSON.parse(data) : null;
  });
  const [token, setToken] = useState(() => localStorage.getItem('token'));

  useEffect(() => {
    if (user) localStorage.setItem('user', JSON.stringify(user));
    else localStorage.removeItem('user');
    if (token) localStorage.setItem('token', token);
    else localStorage.removeItem('token');
  }, [user, token]);

  const login = async (username, password) => {
    const res = await axios.post('http://localhost:8000/auth/login', new URLSearchParams({ username, password }));
    setToken(res.data.access_token);
    // Decode token for role (demo only)
    const payload = JSON.parse(atob(res.data.access_token.split('.')[1]));
    setUser({ username: payload.sub, role: payload.role });
  };

  const logout = () => {
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

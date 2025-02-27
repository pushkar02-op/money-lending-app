// src/App.js
import React, { useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./pages/Login";
import AdminDashboard from "./pages/AdminDashboard";
import AgentDashboard from "./pages/AgentDashboard";
import DashboardLayout from "./components/DashboardLayout";

export const AuthContext = React.createContext();

function App() {
  const [auth, setAuth] = useState({
    token: null,
    role: null,
  });

  return (
    <AuthContext.Provider value={{ auth, setAuth }}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/admin/*"
            element={
              auth.token && auth.role === "admin" ? (
                <DashboardLayout role="admin">
                  <AdminDashboard />
                </DashboardLayout>
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/agent/*"
            element={
              auth.token && auth.role === "agent" ? (
                <DashboardLayout role="agent">
                  <AgentDashboard />
                </DashboardLayout>
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthContext.Provider>
  );
}

export default App;

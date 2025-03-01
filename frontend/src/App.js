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
import ManageUsers from "./pages/ManageUsers";
import AgentDashboard from "./pages/AgentDashboard";
import NewLoan from "./pages/NewLoan";
import DashboardLayout from "./components/DashboardLayout";

export const AuthContext = React.createContext();

function App() {
  const [auth, setAuth] = useState({
    token: null,
    role: null,
    user_id: null, // Ensure you store the user ID here after login
  });

  return (
    <AuthContext.Provider value={{ auth, setAuth }}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          {auth.token && auth.role === "admin" ? (
            <Route path="/admin/*" element={<DashboardLayout role="admin" />}>
              <Route index element={<AdminDashboard />} />
              <Route path="manage-users" element={<ManageUsers />} />
            </Route>
          ) : (
            <Route path="/admin/*" element={<Navigate to="/login" replace />} />
          )}
          {auth.token && auth.role === "agent" ? (
            <Route path="/agent/*" element={<DashboardLayout role="agent" />}>
              <Route index element={<AgentDashboard />} />
              <Route path="new-loan" element={<NewLoan />} />
            </Route>
          ) : (
            <Route path="/agent/*" element={<Navigate to="/login" replace />} />
          )}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthContext.Provider>
  );
}

export default App;

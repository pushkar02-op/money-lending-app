// src/pages/AgentDashboard.js
import React from "react";
import { Paper, Typography } from "@mui/material";

function AgentDashboard() {
  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Agent Overview
      </Typography>
      <Typography>
        Welcome to the agent dashboard. Here you can view your loans, update
        statuses, and track repayments.
      </Typography>
    </Paper>
  );
}

export default AgentDashboard;

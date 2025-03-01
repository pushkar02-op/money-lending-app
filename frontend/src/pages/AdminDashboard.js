// src/pages/AdminDashboard.js
import React, { useEffect, useState } from "react";
import { Box, Typography, CircularProgress } from "@mui/material";
import KeyMetrics from "../components/KeyMetrics";
import LoansTable from "../components/LoansTable";
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";

function AdminDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loadingMetrics, setLoadingMetrics] = useState(false);

  // Define summary state variables
  const [summary, setSummary] = useState([]);
  const [loadingSummary, setLoadingSummary] = useState(false);

  const fetchMetrics = async () => {
    setLoadingMetrics(true);
    try {
      const response = await fetch("http://localhost:8000/loans/metrics");
      if (response.ok) {
        const data = await response.json();
        setMetrics(data);
      } else {
        console.error("Failed to fetch metrics");
      }
    } catch (err) {
      console.error("Error fetching metrics:", err);
    }
    setLoadingMetrics(false);
  };

  const fetchSummary = async () => {
    setLoadingSummary(true);
    try {
      const response = await fetch("http://localhost:8000/loans/summary");
      if (response.ok) {
        const data = await response.json();
        setSummary(data);
      } else {
        console.error("Failed to fetch summary");
      }
    } catch (err) {
      console.error("Error fetching summary:", err);
    }
    setLoadingSummary(false);
  };

  useEffect(() => {
    fetchMetrics();
    fetchSummary();
  }, []);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>
      {/* Global Metrics Component */}
      {loadingMetrics ? (
        <Box sx={{ display: "flex", justifyContent: "center", my: 2 }}>
          <CircularProgress />
        </Box>
      ) : metrics ? (
        <KeyMetrics metrics={metrics} />
      ) : null}

      {/* Loans Table Component */}
      <LoansTable
        onRefreshMetrics={() => {
          fetchMetrics();
          fetchSummary();
        }}
      />

      {/* Summary of Outstanding Loans per Agent */}
      <Paper elevation={3} sx={{ p: 3, mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Outstanding Loans by Agent
        </Typography>
        {loadingSummary ? (
          <Box sx={{ display: "flex", justifyContent: "center", my: 2 }}>
            <CircularProgress />
          </Box>
        ) : (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Agent</TableCell>
                  <TableCell>Total Outstanding</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {summary.map((entry) => (
                  <TableRow key={entry.agent_name}>
                    <TableCell>{entry.agent_name}</TableCell>
                    <TableCell>₹ {entry.total_outstanding}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>
    </Box>
  );
}

export default AdminDashboard;

import React, { useEffect, useState } from "react";
import {
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  CircularProgress,
  Box,
} from "@mui/material";
import KeyMetrics from "../components/KeyMetrics";

function AdminDashboard() {
  const [loans, setLoans] = useState([]);
  const [summary, setSummary] = useState([]);
  const [loadingLoans, setLoadingLoans] = useState(false);
  const [loadingSummary, setLoadingSummary] = useState(false);
  const [error, setError] = useState("");

  const fetchLoans = async () => {
    setLoadingLoans(true);
    setError("");
    try {
      const response = await fetch("http://localhost:8000/loans");
      if (!response.ok) {
        const err = await response.json();
        setError(err.detail || "Failed to fetch loans");
      } else {
        const data = await response.json();
        setLoans(data);
      }
    } catch (err) {
      setError("Error fetching loans");
    }
    setLoadingLoans(false);
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
    fetchLoans();
    fetchSummary();
  }, []);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>
      <KeyMetrics loans={loans} />

      {/* Detailed Loans Table */}
      <Paper elevation={3} sx={{ p: 3, mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Loans Summary
        </Typography>
        <Button
          variant="contained"
          onClick={() => {
            fetchLoans();
            fetchSummary();
          }}
          sx={{ mb: 2 }}
        >
          Refresh Data
        </Button>
        {loadingLoans ? (
          <Box sx={{ display: "flex", justifyContent: "center", my: 2 }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Typography color="error">{error}</Typography>
        ) : (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Borrower</TableCell>
                  <TableCell>Agent</TableCell>
                  <TableCell>Amount</TableCell>
                  <TableCell>Loan Date</TableCell>
                  <TableCell>Interest Rate (%)</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Repayment</TableCell>
                  <TableCell>Remaining Balance</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loans.map((loan) => (
                  <TableRow key={loan.id}>
                    <TableCell>
                      {loan.borrower_name || loan.borrower_id}
                    </TableCell>
                    <TableCell>{loan.agent_name || loan.agent_id}</TableCell>
                    <TableCell>{loan.amount}</TableCell>
                    <TableCell>{loan.loan_date}</TableCell>
                    <TableCell>{loan.interest_rate}</TableCell>
                    <TableCell>{loan.status}</TableCell>
                    <TableCell>
                      {loan.repayment_method === "interest"
                        ? `${loan.payment_frequency || "N/A"}`
                        : "full"}
                    </TableCell>
                    <TableCell>{loan.remaining_balance}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>

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

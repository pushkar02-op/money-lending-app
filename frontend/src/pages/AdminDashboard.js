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

function AdminDashboard() {
  const [loans, setLoans] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Fetch loans from the backend API
  const fetchLoans = async () => {
    setLoading(true);
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
    setLoading(false);
  };

  useEffect(() => {
    fetchLoans();
  }, []);

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Admin Overview – Loans Summary
      </Typography>
      <Button variant="contained" onClick={fetchLoans} sx={{ mb: 2 }}>
        Refresh Data
      </Button>
      {loading ? (
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
                <TableCell>Loan ID</TableCell>
                <TableCell>Borrower</TableCell>
                <TableCell>Agent</TableCell>
                <TableCell>Amount</TableCell>
                <TableCell>Loan Date</TableCell>
                <TableCell>Due Date</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loans.map((loan) => (
                <TableRow key={loan.id}>
                  <TableCell>{loan.id}</TableCell>
                  <TableCell>
                    {loan.borrower_name || loan.borrower_id}
                  </TableCell>
                  <TableCell>{loan.agent_name || loan.agent_id}</TableCell>
                  <TableCell>{loan.amount}</TableCell>
                  <TableCell>{loan.loan_date}</TableCell>
                  <TableCell>{loan.due_date}</TableCell>
                  <TableCell>{loan.status}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Paper>
  );
}

export default AdminDashboard;

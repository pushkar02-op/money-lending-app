/**
 * Agent Dashboard:
 *
 * - Fetches and displays loans assigned to the agent.
 * - Shows outstanding loan balances dynamically.
 * - Allows agents to record payments for loans.
 */

import React, { useEffect, useState } from "react";
import {
  Paper,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from "@mui/material";

function AgentDashboard() {
  const [loans, setLoans] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedLoan, setSelectedLoan] = useState(null);
  const [paymentAmount, setPaymentAmount] = useState("");

  useEffect(() => {
    fetchLoans();
  }, []);

  const fetchLoans = async () => {
    try {
      const response = await fetch("http://localhost:8000/loans");
      const data = await response.json();
      setLoans(data);
      console.log(data);
    } catch (err) {
      console.error("Failed to fetch loans");
    }
  };

  const handleOpenDialog = (loan) => {
    setSelectedLoan(loan);
    setPaymentAmount("");
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedLoan(null);
  };

  const handlePaymentSubmit = async () => {
    if (!paymentAmount || isNaN(paymentAmount) || paymentAmount <= 0) {
      alert("Please enter a valid payment amount.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/payments/pay", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          loan_id: selectedLoan.id,
          amount_paid: parseFloat(paymentAmount),
        }),
      });

      const result = await response.json();

      if (response.ok) {
        alert(
          `Payment recorded successfully. New Balance: ₹${result.remaining_balance}`
        );
        fetchLoans(); // Refresh loan data after payment
        handleCloseDialog();
      } else {
        alert(result.detail || "Error processing payment.");
      }
    } catch (err) {
      alert("Failed to record payment.");
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Agent Dashboard
      </Typography>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Loan ID</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Remaining Balance</TableCell>
              <TableCell>Repayment</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loans.map((loan) => (
              <TableRow key={loan.id}>
                <TableCell>{loan.id}</TableCell>
                <TableCell>{loan.amount}</TableCell>
                <TableCell>{loan.remaining_balance ?? "N/A"}</TableCell>
                <TableCell>
                  <Button
                    variant="contained"
                    onClick={() => handleOpenDialog(loan)}
                  >
                    Record Payment
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Payment Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Record Payment</DialogTitle>
        <DialogContent>
          <Typography>
            Loan ID: {selectedLoan?.id} | Remaining Balance: ₹
            {selectedLoan?.remaining_balance}
          </Typography>
          <TextField
            fullWidth
            label="Payment Amount"
            type="number"
            value={paymentAmount}
            onChange={(e) => setPaymentAmount(e.target.value)}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="secondary">
            Cancel
          </Button>
          <Button onClick={handlePaymentSubmit} color="primary">
            Submit Payment
          </Button>
        </DialogActions>
      </Dialog>
    </Paper>
  );
}

export default AgentDashboard;

// src/pages/NewLoan.js
import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../App";
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  MenuItem,
  Box,
  FormControl,
  InputLabel,
  Select,
} from "@mui/material";

function NewLoan() {
  const { auth } = useContext(AuthContext);
  const navigate = useNavigate();

  // Form fields state
  const [borrowerName, setBorrowerName] = useState("");
  const [borrowerContact, setBorrowerContact] = useState("");
  const [amount, setAmount] = useState("");
  const [interestRate, setInterestRate] = useState("");
  const [repaymentMethod, setRepaymentMethod] = useState("full");
  const [paymentFrequency, setPaymentFrequency] = useState("");
  const [loanDate, setLoanDate] = useState(
    new Date().toISOString().slice(0, 10)
  ); // New state for date picker
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!borrowerName || !amount || !interestRate) {
      setError("Please fill in all required fields.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/loans/issue", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${auth.token}`,
        },
        body: JSON.stringify({
          borrower_name: borrowerName,
          borrower_contact: borrowerContact,
          amount: parseFloat(amount),
          interest_rate: parseFloat(interestRate),
          repayment_method: repaymentMethod,
          payment_frequency:
            repaymentMethod === "interest" ? paymentFrequency : null,
          agent_id: auth.user_id,
          loan_date: loanDate, // Pass the selected loan date
        }),
      });

      if (!response.ok) {
        const errData = await response.json();
        setError(
          typeof errData.detail === "object"
            ? JSON.stringify(errData.detail)
            : errData.detail || "Error issuing loan"
        );
        return;
      }

      const data = await response.json();
      alert(data.message || "Loan issued successfully!");
      navigate("/agent");
    } catch (err) {
      console.error("Error creating loan:", err);
      setError("Error creating loan");
    }
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 4, mt: 8 }}>
        <Typography variant="h5" gutterBottom>
          Issue New Loan
        </Typography>
        {error && (
          <Typography color="error" variant="body2" sx={{ mb: 2 }}>
            {error}
          </Typography>
        )}
        <Box component="form" onSubmit={handleSubmit} noValidate>
          {/* Borrower Fields */}
          <TextField
            margin="normal"
            required
            fullWidth
            label="Borrower Name"
            value={borrowerName}
            onChange={(e) => setBorrowerName(e.target.value)}
          />
          <TextField
            margin="normal"
            fullWidth
            label="Borrower Contact"
            value={borrowerContact}
            onChange={(e) => setBorrowerContact(e.target.value)}
          />

          {/* Loan Fields */}
          <TextField
            margin="normal"
            required
            fullWidth
            label="Loan Amount"
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            label="Interest Rate (%)"
            type="number"
            value={interestRate}
            onChange={(e) => setInterestRate(e.target.value)}
          />

          {/* New Date Picker Field */}
          <TextField
            margin="normal"
            required
            fullWidth
            label="Loan Date"
            type="date"
            value={loanDate}
            onChange={(e) => setLoanDate(e.target.value)}
            InputLabelProps={{
              shrink: true,
            }}
          />

          {/* Repayment Method */}
          <FormControl fullWidth margin="normal">
            <InputLabel>Repayment Method</InputLabel>
            <Select
              label="Repayment Method"
              value={repaymentMethod}
              onChange={(e) => setRepaymentMethod(e.target.value)}
            >
              <MenuItem value="full">Full</MenuItem>
              <MenuItem value="interest">Interest</MenuItem>
            </Select>
          </FormControl>

          {/* Payment Frequency (if repayment is interest) */}
          {repaymentMethod === "interest" && (
            <FormControl fullWidth margin="normal">
              <InputLabel>Payment Frequency</InputLabel>
              <Select
                label="Payment Frequency"
                value={paymentFrequency}
                onChange={(e) => setPaymentFrequency(e.target.value)}
              >
                <MenuItem value="daily">Daily</MenuItem>
                <MenuItem value="monthly">Monthly</MenuItem>
              </Select>
            </FormControl>
          )}

          <Button type="submit" fullWidth variant="contained" sx={{ mt: 3 }}>
            Issue Loan
          </Button>
        </Box>
      </Paper>
    </Container>
  );
}

export default NewLoan;

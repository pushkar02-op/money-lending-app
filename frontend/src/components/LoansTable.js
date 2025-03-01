// src/components/LoansTable.js
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
  TablePagination,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";

const LoansTable = ({ onRefreshMetrics }) => {
  const [loans, setLoans] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Pagination and filtering state
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [filterStatus, setFilterStatus] = useState("All");

  const fetchLoans = async () => {
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams();
      params.append("skip", page * rowsPerPage);
      params.append("limit", rowsPerPage);
      if (filterStatus !== "All") {
        params.append("status", filterStatus.toLowerCase());
      }
      const response = await fetch(
        `http://localhost:8000/loans?${params.toString()}`
      );
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

  // Re-fetch loans when pagination or filter changes
  useEffect(() => {
    fetchLoans();
  }, [page, rowsPerPage, filterStatus]);

  const handleRefresh = () => {
    fetchLoans();
    if (onRefreshMetrics) {
      onRefreshMetrics();
    }
  };

  const handlePageChange = (event, newPage) => {
    setPage(newPage);
  };

  const handleRowsPerPageChange = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 4 }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Typography variant="h5" gutterBottom>
          Loans
        </Typography>
        <FormControl sx={{ minWidth: 150 }}>
          <InputLabel>Status Filter</InputLabel>
          <Select
            label="Status Filter"
            value={filterStatus}
            onChange={(e) => {
              setFilterStatus(e.target.value);
              setPage(0);
            }}
          >
            <MenuItem value="All">All</MenuItem>
            <MenuItem value="active">Active</MenuItem>
            <MenuItem value="completed">Completed</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Button variant="contained" onClick={handleRefresh} sx={{ mb: 2 }}>
        Refresh Table
      </Button>
      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", my: 2 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Typography color="error">{error}</Typography>
      ) : (
        <>
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
          <TablePagination
            component="div"
            count={-1} // Update this if the API provides a total count
            page={page}
            onPageChange={handlePageChange}
            rowsPerPage={rowsPerPage}
            onRowsPerPageChange={handleRowsPerPageChange}
            labelDisplayedRows={({ from, to }) => `${from}-${to}`}
            nextIconButtonProps={{ disabled: loans.length < rowsPerPage }}
          />
        </>
      )}
    </Paper>
  );
};

export default LoansTable;

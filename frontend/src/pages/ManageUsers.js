// src/pages/ManageUsers.js
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

function ManageUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchUsers = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch("http://localhost:8000/users");
      if (!response.ok) {
        const err = await response.json();
        setError(err.detail || "Failed to fetch users");
      } else {
        const data = await response.json();
        setUsers(data);
      }
    } catch (err) {
      setError("Error fetching users");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Manage Users
      </Typography>
      <Button variant="contained" onClick={fetchUsers} sx={{ mb: 2 }}>
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
                <TableCell>User ID</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Role</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>{user.id}</TableCell>
                  <TableCell>{user.name}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>{user.role}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Paper>
  );
}

export default ManageUsers;

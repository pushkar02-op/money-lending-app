// src/pages/ManageUsers.js
import React, { useEffect, useState, useContext } from "react";
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
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import { AuthContext } from "../App";

function ManageUsers() {
  const { auth } = useContext(AuthContext);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Form state for adding a new agent
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [adding, setAdding] = useState(false);
  const [addError, setAddError] = useState("");

  // State for transfer dialog when deleting an agent
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedAgentToDelete, setSelectedAgentToDelete] = useState(null);
  const [transferAgentId, setTransferAgentId] = useState("");
  const [deleteError, setDeleteError] = useState("");

  // Fetch all users
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

  // Handle adding a new agent using /auth/register endpoint
  const handleAddAgent = async (e) => {
    e.preventDefault();
    setAddError("");
    setAdding(true);
    try {
      const response = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // Include the admin token here!
          Authorization: `Bearer ${auth.token}`,
        },
        body: JSON.stringify({
          name,
          email,
          password,
          role: "agent", // Force role to agent
        }),
      });
      if (!response.ok) {
        const err = await response.json();
        setAddError(err.detail || "Failed to add agent");
      } else {
        // Clear form and refresh users list
        setName("");
        setEmail("");
        setPassword("");
        fetchUsers();
      }
    } catch (err) {
      setAddError("Error adding agent");
    }
    setAdding(false);
  };

  // Open dialog for deleting an agent
  const openDeleteDialog = (agent) => {
    setSelectedAgentToDelete(agent);
    setTransferAgentId(""); // Reset selection
    setDeleteError("");
    setOpenDialog(true);
  };

  const closeDeleteDialog = () => {
    setOpenDialog(false);
    setSelectedAgentToDelete(null);
    setTransferAgentId("");
    setDeleteError("");
  };

  // Handle deletion of an agent using the DELETE /users/{id} endpoint with optional transfer
  const handleDeleteAgent = async () => {
    if (!selectedAgentToDelete) return;
    try {
      let url = `http://localhost:8000/users/${selectedAgentToDelete.id}`;
      if (transferAgentId) {
        url += `?transfer_agent_id=${transferAgentId}`;
      }
      const response = await fetch(url, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${auth.token}`,
        },
      });
      if (!response.ok) {
        const err = await response.json();
        setDeleteError(err.detail || "Failed to delete agent");
      } else {
        closeDeleteDialog();
        fetchUsers();
      }
    } catch (err) {
      setDeleteError("Error deleting agent");
    }
  };

  // Filter only agent users for the transfer dropdown (exclude the agent being deleted)
  const otherAgents = users.filter(
    (user) =>
      user.role === "agent" &&
      user.id !== (selectedAgentToDelete ? selectedAgentToDelete.id : null)
  );

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Manage Users
      </Typography>

      {/* Add New Agent Form */}
      <Box component="form" onSubmit={handleAddAgent} sx={{ mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Add New Agent
        </Typography>
        <TextField
          label="Name"
          fullWidth
          value={name}
          onChange={(e) => setName(e.target.value)}
          margin="normal"
          required
        />
        <TextField
          label="Email"
          type="email"
          fullWidth
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          margin="normal"
          required
        />
        <TextField
          label="Password"
          type="password"
          fullWidth
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          margin="normal"
          required
        />
        {addError && (
          <Typography color="error" variant="body2">
            {addError}
          </Typography>
        )}
        <Button
          type="submit"
          variant="contained"
          sx={{ mt: 2 }}
          disabled={adding}
        >
          {adding ? "Adding..." : "Add Agent"}
        </Button>
      </Box>

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
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>{user.id}</TableCell>
                  <TableCell>{user.name}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>{user.role}</TableCell>
                  <TableCell>
                    {user.role === "agent" && (
                      <Button
                        variant="contained"
                        color="error"
                        onClick={() => openDeleteDialog(user)}
                      >
                        Remove
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Delete Confirmation Dialog with Transfer Option */}
      <Dialog open={openDialog} onClose={closeDeleteDialog}>
        <DialogTitle>Delete Agent</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete agent{" "}
            {selectedAgentToDelete ? selectedAgentToDelete.name : ""}?
          </Typography>
          <Typography variant="body2" sx={{ mt: 2 }}>
            If this agent has borrowers assigned, please select another agent to
            transfer them.
          </Typography>
          {otherAgents.length > 0 ? (
            <FormControl fullWidth sx={{ mt: 2 }}>
              <InputLabel>Transfer To</InputLabel>
              <Select
                label="Transfer To"
                value={transferAgentId}
                onChange={(e) => setTransferAgentId(e.target.value)}
              >
                {otherAgents.map((agent) => (
                  <MenuItem key={agent.id} value={agent.id}>
                    {agent.name} ({agent.email})
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          ) : (
            <Typography variant="body2" color="error" sx={{ mt: 2 }}>
              No other agents available for transfer.
            </Typography>
          )}
          {deleteError && (
            <Typography color="error" variant="body2" sx={{ mt: 2 }}>
              {deleteError}
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={closeDeleteDialog}>Cancel</Button>
          <Button onClick={handleDeleteAgent} variant="contained" color="error">
            Delete Agent
          </Button>
        </DialogActions>
      </Dialog>
    </Paper>
  );
}

export default ManageUsers;

// src/components/DashboardLayout.js
import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../App";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Drawer,
  List,
  ListItem,
  ListItemText,
  Box,
  CssBaseline,
} from "@mui/material";

const drawerWidth = 240;

const DashboardLayout = ({ role, children }) => {
  const { setAuth } = React.useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    setAuth({ token: null, role: null });
    navigate("/login");
  };

  const menuItems =
    role === "admin"
      ? [
          { text: "Overview", link: "/admin" },
          { text: "Manage Users", link: "/admin/manage-users" },
        ]
      : [
          { text: "Overview", link: "/agent" },
          { text: "My Loans", link: "/agent/loans" },
        ];

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          width: `calc(100% - ${drawerWidth}px)`,
          ml: `${drawerWidth}px`,
        }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            {role === "admin" ? "Admin Dashboard" : "Agent Dashboard"}
          </Typography>
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: "auto" }}>
          <List>
            {menuItems.map((item, index) => (
              <ListItem button key={index} component={Link} to={item.link}>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default DashboardLayout;

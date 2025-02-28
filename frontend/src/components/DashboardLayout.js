import React, { useState } from "react";
import { Link, useNavigate, useLocation, Outlet } from "react-router-dom";
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
  IconButton,
  Divider,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";

const drawerWidth = 240;

const DashboardLayout = ({ role }) => {
  const { setAuth } = React.useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };

  const handleLogout = () => {
    setAuth({ token: null, role: null, user_id: null });
    navigate("/login");
  };

  // Updated menu items: For agents, add "Issue Loan" along with other options.
  const menuItems =
    role === "admin"
      ? [
          { text: "Overview", link: "/admin" },
          { text: "Manage Users", link: "/admin/manage-users" },
        ]
      : [
          { text: "Overview", link: "/agent" },
          { text: "My Loans", link: "/agent/loans" },
          { text: "Issue Loan", link: "/agent/new-loan" },
        ];

  const drawer = (
    <div>
      <Toolbar />
      <Divider />
      <List>
        {menuItems.map((item, index) => (
          <ListItem
            button
            key={index}
            component={Link}
            to={item.link}
            selected={
              location.pathname === item.link ||
              location.pathname.startsWith(item.link + "/")
            }
            onClick={() => setDrawerOpen(false)}
          >
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ width: "100%" }}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap sx={{ flexGrow: 1 }}>
            {role === "admin" ? "Admin Dashboard" : "Agent Dashboard"}
          </Typography>
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="temporary"
        open={drawerOpen}
        onClose={handleDrawerToggle}
        ModalProps={{ keepMounted: true }}
        sx={{
          "& .MuiDrawer-paper": {
            boxSizing: "border-box",
            width: drawerWidth,
          },
        }}
      >
        {drawer}
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
        <Outlet />
      </Box>
    </Box>
  );
};

export default DashboardLayout;

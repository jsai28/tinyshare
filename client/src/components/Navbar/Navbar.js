import { AppBar, Typography } from "@mui/material";
import "./Navbar.css";

function Navbar() {
  return (
    <AppBar position="static" sx={{ bgcolor: "#152238" }}>
      <Typography variant="h4">TinySha.re</Typography>
    </AppBar>
  );
}

export default Navbar;

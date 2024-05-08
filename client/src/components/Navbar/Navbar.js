import { AppBar, Typography } from "@mui/material";
import "./Navbar.css";

function Navbar() {
  return (
    <AppBar position="static" sx={{ bgcolor: "#3e73d9", textAlign: "center" }}>
      <Typography variant="h4">TinyShare</Typography>
    </AppBar>
  );
}

export default Navbar;

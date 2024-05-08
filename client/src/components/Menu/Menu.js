import { useState } from "react";
import { TextField, Button, Paper, Grid, Typography } from "@mui/material";
import axios from "axios";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

import "./Menu.css";

const baseURL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:5000/"
    : window.location.origin;

function Menu() {
  const [originalURL, setOriginalURL] = useState("");
  const [password, setPassword] = useState(null);
  const [expiryDate, setExpiryDate] = useState(null);
  const [tinyshareURL, setTinyshareURL] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await axios.post(`${baseURL}/link`, {
        title: "title",
        description: "description",
        original_url: originalURL,
        password: password,
        expiry_date: expiryDate,
      });
      setTinyshareURL(baseURL + "/" + data.data.tinyshare_url);
    } catch (err) {
      console.error(err.message);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(tinyshareURL);
  };

  return (
    <>
      <Grid className="grid">
        <Typography variant="h6" align="center">
          Create a short URL with an optional code and expiry date!
        </Typography>
      </Grid>
      <Paper elevation={3} className="menu" sx={{ borderRadius: "30px" }}>
        <Grid container direction="column">
          <form onSubmit={handleSubmit}>
            <Grid className="title">
              <Typography variant="h5">Original URL</Typography>
            </Grid>
            <TextField
              className="title"
              label="Enter URL Here"
              onChange={(e) => setOriginalURL(e.target.value)}
              type="text"
              name="Original URL"
              id="originalURL"
              value={originalURL}
              fullWidth
              required
              variant="filled"
            />
            <Grid className="title2">
              <Typography variant="h5">Secret Code</Typography>
            </Grid>
            <TextField
              label="Enter Code"
              onChange={(e) => setPassword(e.target.value)}
              type="text"
              name="Password"
              id="password"
              fullWidth
              variant="filled"
            />
            <Grid className="title3">
              <Typography variant="h5">Expiry Date</Typography>
            </Grid>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DatePicker
                label="Select Expiry Date"
                onChange={(e) => {
                  setExpiryDate(e);
                }}
                disablePast
              />
            </LocalizationProvider>
            <Button
              className="submit"
              variant="contained"
              fullWidth
              type="submit"
              sx={{ margin: "15px 0px 0px", background: "#3e73d9" }}
            >
              Submit
            </Button>
          </form>
          <hr />
          <Typography variant="h5">TinyShare URL</Typography>
          <Grid container spacing={1} alignItems="center">
            <Grid item xs={9}>
              <TextField
                fullWidth
                value={`${tinyshareURL}`}
                InputProps={{
                  readOnly: true,
                }}
                sx={{
                  ".MuiInputBase-input": { fontWeight: "bold" },
                }}
              />
            </Grid>
            <Grid item xs={2}>
              <Button
                variant="contained"
                className="copy"
                sx={{ background: "#3e73d9" }}
                onClick={handleCopy}
              >
                Copy
              </Button>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
    </>
  );
}

export default Menu;

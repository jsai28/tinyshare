import "./App.css";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import Navbar from "./components/Navbar/Navbar";
import Menu from "./components/Menu/Menu";

const theme = createTheme({
  typography: {
    fontFamily: "Roboto Mono, monospace", // Applies Roboto Mono globally
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div className="App">
        <Navbar />
        <Menu />
      </div>
    </ThemeProvider>
  );
}

export default App;

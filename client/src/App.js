import { useEffect, useState } from "react";
import axios from "axios";
import { format } from "date-fns";

import "./App.css";

const baseURL = "http://localhost:5000";

function App() {
  const [originalURL, setOriginalURL] = useState("");
  const [tinyshareURL, setTinyshareURL] = useState("");

  const fetchLink = async () => {
    const data = await axios.get(`${baseURL}/link`);
  };

  const handleChange = (e) => {
    setOriginalURL(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await axios.post(`${baseURL}/link`, {
        title: "title",
        description: "description",
        original_url: originalURL,
      });
      console.log(data);
      setTinyshareURL(data.data.tinyshare_url);
    } catch (err) {
      console.error(err.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <form onSubmit={handleSubmit}>
          <label htmlFor="originalURL">URL</label>
          <input
            onChange={handleChange}
            type="text"
            name="Original URL"
            id="originalURL"
            value={originalURL}
          />
          <button type="submit">Submit</button>
        </form>
        <label htmlFor="tinyshareURL">TinyShare URL:</label>
        <p>
          `{baseURL}/{tinyshareURL}`
        </p>
      </header>
    </div>
  );
}

export default App;

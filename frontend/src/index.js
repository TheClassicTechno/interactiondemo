
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// Get the root DOM node
const root = ReactDOM.createRoot(document.getElementById("root"));

// Render the App component inside React.StrictMode for highlighting potential problems
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

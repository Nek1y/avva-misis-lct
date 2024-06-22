import { createRoot } from "react-dom/client";

import { BrowserRouter } from "react-router-dom";
import './common/net';
import "./index.css";
import App from "./App";

const node = document.getElementById("root");
const root = createRoot(node);

root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);

import React, { createContext } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import Home from "./components/Home";
import Game from "./components/Game";
import Registration from "./components/Registration";
import "./App.css";

export const AppContext = createContext<{ login: string, password: string, formValid: boolean }>({
  login: '',
  password: '',
  formValid: false
});

const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement);
root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/auth" element={<App />} />
      <Route path="/registration" element={<Registration />} />
      <Route path="/game" element={<Game />} />
    </Routes>
  </BrowserRouter>
);

import React from "react";
import { useNavigate } from "react-router-dom";
import logo from "../../logo.svg";
import "./Header.css";

function Header() {
  const navigate = useNavigate();

  return (
    <header className="App-header">
      <img src={logo} className="App-logo" alt="logo" />
      <button onClick={() => navigate("/login")}>Login</button>
    </header>
  );
}

export default Header;

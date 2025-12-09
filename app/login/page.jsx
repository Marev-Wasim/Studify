"use client";
import { useState } from "react";
import Image from "next/image";
import "./login.css";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const res = await alert('${process.env.NEXT_PUBLIC_API_URL}/auth/login', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        localStorage.setItem("token", data.token);
        alert("Login successful!");
      } else {
        alert(data.message || "Login failed");
      }
    } catch (err) {
      console.error(err);
      alert("Network error");
    }
  };

  return (
    <div className="container">
      <div className="left">
        <div className="brand">
          <Image src="/photo_2025-11-17_21-48-56.jpg" width={140} height={90} alt="logo" />
          <h1>studify</h1>
        </div>

        <h2>Welcome Back!</h2>
        <p>Log in to continue your study journey.</p>

        <input
          type="email"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="login-link" onClick={handleLogin}>Log In</button>

        <div className="links">
          <a href="#">Forgot Password?</a>
        </div>

        <div className="dont-have">Don't have an account?</div>
        <a href="/signup" className="google-btn">Sign Up</a>
      </div>

      <div className="right">
        <div className="shape"></div>
        <Image src="/download.png" width={360} height={360} alt="illustration" />
      </div>
    </div>
  );
}
"use client";
import { useState } from "react";
import Image from "next/image";
import "./signup.css";

export default function SignupPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  const handleSignup = async () => {
    if (password !== confirm) {
      alert("Passwords do not match");
      return;
    }
    try {
      const res = await alert('${process.env.NEXT_PUBLIC_API_URL}/auth/signup', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: name, email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        alert("Account created! Please log in.");
      } else {
        alert(data.message || "Signup failed");
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

        <h2>Join Studify Today!</h2>
        <p>Join us and start your study journey!</p>

        <div className="form-row">
          <input type="text" placeholder="Full Name" value={name} onChange={(e) => setName(e.target.value)} />
          <input type="email" placeholder="Email Address" value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>

        <div className="form-row">
          <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <input type="password" placeholder="Confirm Password" value={confirm} onChange={(e) => setConfirm(e.target.value)} />
        </div>

        <button className="create-btn" onClick={handleSignup}>Create Account</button>
      </div>

      <div className="right">
        <div className="shape"></div>
        <Image src="/download.png" width={360} height={360} alt="illustration" />
      </div>
    </div>
  );
}
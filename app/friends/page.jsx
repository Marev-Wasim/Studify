"use client";
import { useEffect, useState } from "react";
import "./friends.css";

export default function FriendPage() {
  const [friends, setFriends] = useState([]);
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    fetchFriends();
    fetchRequests();
  }, []);

  const fetchFriends = async () => {
    try {
      const res = await fetch("https://your-backend.com/api/friends");
      const data = await res.json();
      setFriends(data);
    } catch (err) {
      console.error("Error fetching friends:", err);
    }
  };

  const fetchRequests = async () => {
    try {
      const res = await fetch("https://your-backend.com/api/requests");
      const data = await res.json();
      setRequests(data);
    } catch (err) {
      console.error("Error fetching requests:", err);
    }
  };

  const handleAccept = async (id) => {
    try {
      await fetch('https://your-backend.com/api/requests/${id}/accept', { method: 'POST' });
      fetchRequests(); // تحديث القائمة بعد الموافقة
    } catch (err) {
      console.error(err);
    }
  };

  const handleDecline = async (id) => {
    try {
      await fetch('https://your-backend.com/api/requests/${id}/decline', { method: 'POST' });
      fetchRequests(); // تحديث القائمة بعد الرفض
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="container">
      {/* Header */}
      <header>
        <div className="logo-section">
          <img
            src="https://api.builder.io/api/v1/image/assets/TEMP/3205192e6eb58326a0090867bfed104d8aa10659?width=256"
            alt="Studify Logo"
          />
          <h1>studify</h1>
        </div>

        <nav>
          <a href="/profile">Profile</a>
          <a href="#home">Home</a>
          <a href="#about">About us</a>
        </nav>
      </header>

      {/* Main Grid */}
      <div className="main-grid">
        {/* Friends Section */}
        <div className="friends-section">
          <h2 id="listTitle">My Friends</h2>

          <div className="search-add-wrapper">
            <div className="search-container">
              <div className="search-icon">
                <svg width={18} height={19} viewBox="0 0 18 19" fill="none">
                  <ellipse cx="9" cy="9.5" rx="9" ry="9.5" fill="#FCF8FA" />
                  <path
                    d="M9 0.5C13.6693 0.5 17.5 4.50362 17.5 9.5C17.5 14.4964 13.6693 18.5 9 18.5C4.33071 18.5 0.5 14.4964 0.5 9.5C0.5 4.50362 4.33071 0.5 9 0.5Z"
                    stroke="black"
                    strokeOpacity="0.22"
                  />
                </svg>
              </div>

              <input
                type="text"
                className="search-input"
                placeholder="Search new friends to add..."
                id="searchInput"
              />
            </div>

            <button
              className="add-friend-btn"
              onClick={() => document.getElementById("searchInput").focus()}
            >
              Add Friend
            </button>
          </div>

          <div className="all-friends-tab">
            <button className="tab-btn" id="tabBtn">All Friends</button>
          </div>

          <div className="friends-grid" id="friendsContainer">
            {friends.length > 0 ? (
              friends.map((friend, i) => (
                <div key={i} className="friend-card">
                  <img src={friend.avatar} alt="" />
                  <h3>{friend.name}</h3>
                </div>
              ))
            ) : (
              <p>No friends found.</p>
            )}
          </div>
        </div>

        {/* Requests Section */}
        <div className="requests-section">
          <h2>Friend Requests</h2>
          <div className="requests-card" id="requestsContainer">

          {requests.length > 0 ? (
              requests.map((req, i) => (
                <div key={i} className="request-item">
                  <img src={req.avatar} alt="" />
                  <h3>{req.name}</h3>
                   
  
                  <button
                    onClick={() => handleAccept(req.id)}
                    style={{
                      padding: '8px 16px',
                      backgroundColor: '#3EC1D3',
                      color: 'white',
                      border: 'none',
                      borderRadius: '8px',
                      cursor: 'pointer',
                      marginRight: '8px'
                    }}
                  >
                    Accept
                  </button>
                  <button
                    onClick={() => handleDecline(req.id)}
                    style={{
                      padding: '8px 16px',
                      backgroundColor: '#FF4B4B',
                      color: 'white',
                      border: 'none',
                      borderRadius: '8px',
                      cursor: 'pointer'
                    }}
                  >
                    Decline
                  </button>
                </div>
              ))
            ) : (
              <p>No friend requests.</p>
            )}
          </div>
        </div>
      </div>

      {/* Decorative Images */}
      <div className="decorative-images">
        <img
          src="https://api.builder.io/api/v1/image/assets/TEMP/2a4e29a6ed62522ae0bbe655b784cf0ff29de36a?width=276"
          alt=""
        />
        <img
          src="https://api.builder.io/api/v1/image/assets/TEMP/2a4e29a6ed62522ae0bbe655b784cf0ff29de36a?width=276"
          alt=""
        />
      </div>
    </div>
  );
}
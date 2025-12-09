import styles from "./page.module.css";
"use client";


import Image from "next/image";
import "./task.css";


export default function Home() {
  return (
    <div className={styles.container}>

      {/* NavBar */}
      <nav className={styles.navbar}>
        <div className={styles.logoSection}>
          <Image src="/photo_2025-11-17_21-48-56.jpg.png" alt="photo_2025-11-17_21-48-56.jpg" width={40} height={40} />
          
          <h1 className={styles.logoText}>studify</h1>
        </div>

        <ul className={styles.navLinks}>
          <li>Profile</li>
          <li>Friends</li>
          <li>About us</li>
        </ul>
      </nav>

      {/* Main Content */}
      <div className={styles.main}>

        {/* Left - Add Subject */}
        <div className={styles.cardSubject}>
          <h3>Add New Subject</h3>
          <input type="text" placeholder="Add new Subject" />
        </div>

        {/* Middle - Calendar Illustration */}
        <div className={styles.calendarWrapper}>
          <Image src="/calendar.png" alt="calendar" width={420} height={260} />
        </div>

        {/* Right - Add Task */}
        <div className={styles.cardTask}>
          <h2>Add New Task</h2>

          <label>Task Name</label>
          <input type="text" placeholder="Task name" />

          <label>Due Date</label>
          <input type="text" placeholder="  /   /" />

          <label>Subject</label>
          <input type="text" placeholder="Subject name" />

          <label>Time</label>
          <input type="text" placeholder="Number of minutes" />
        </div>
      </div>

      {/* Character Illustration */}
      <Image
        src="/student.png"
        alt="student"
        width={180}
        height={180}
        className={styles.student}
      />

      {/* Clouds */}
      <Image src="/cloud.png" alt="cloud" width={120} height={70} className={styles.cloud1} />
      <Image src="/cloud.png" alt="cloud" width={140} height={80} className={styles.cloud2} />
    </div>
  );
}
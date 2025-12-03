import React, { useState, useEffect } from "react";
import "./App.css";

const STORAGE_KEYS = {
  subjects: "studify_subjects_v1",
  tasks: "studify_tasks_v1",
};

function App() {
  const [subjects, setSubjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [newSubject, setNewSubject] = useState("");
  const [taskForm, setTaskForm] = useState({ name: "", date: "", subject: "", time: "" });

  // Load data
  useEffect(() => {
    const savedSubjects = JSON.parse(localStorage.getItem(STORAGE_KEYS.subjects)) || [
      "Math",
      "Physics",
      "English",
    ];
    const savedTasks = JSON.parse(localStorage.getItem(STORAGE_KEYS.tasks)) || [];
    setSubjects(savedSubjects);
    setTasks(savedTasks);
  }, []);

  // Save data
  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.subjects, JSON.stringify(subjects));
  }, [subjects]);
  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.tasks, JSON.stringify(tasks));
  }, [tasks]);

  const addSubject = () => {
    if (!newSubject.trim()) return;
    if (subjects.includes(newSubject.trim())) return alert("المادة مضافة مسبقًا");
    setSubjects([...subjects, newSubject.trim()]);
    setNewSubject("");
  };

  const addTask = () => {
    if (!taskForm.name.trim()) return alert("اكتب اسم المهمة");
    const newTask = { ...taskForm, time: taskForm.time ? Number(taskForm.time) : null };
    setTasks([...tasks, newTask]);
    setTaskForm({ name: "", date: "", subject: "", time: "" });
  };

  const removeTask = (idx) => {
    if (!window.confirm("حذف هذه المهمة؟")) return;
    const updated = [...tasks];
    updated.splice(idx, 1);
    setTasks(updated);
  };

  const removeSubject = (idx) => {
    if (!window.confirm(حذف المادة "${subjects[idx]}"؟)) return;
    const updatedSubjects = [...subjects];
    const removed = updatedSubjects.splice(idx, 1);
    setSubjects(updatedSubjects);
    setTasks(tasks.filter((t) => t.subject !== removed[0]));
  };

  return (
    <div className="frame">
      <div className="div">
        <h2 className="title">Studify</h2>

        <div className="subject-section">
          <h3>Subjects</h3>
          <div className="add-subject">
            <input
              placeholder="Add new subject"
              value={newSubject}
              onChange={(e) => setNewSubject(e.target.value)}
            />
            <button onClick={addSubject}>+</button>
          </div>
          <div className="chips">
            {subjects.map((s, idx) => (
              <div key={idx} className="chip">
                {s} <span onClick={() => removeSubject(idx)}>✕</span>
              </div>
            ))}
          </div>
        </div>

        <div className="task-section">
          <h3>Tasks</h3>
          <div className="add-task">
            <input
              placeholder="Task name"
              value={taskForm.name}
              onChange={(e) => setTaskForm({ ...taskForm, name: e.target.value })}
            />
            <input
              type="date"
              value={taskForm.date}
              onChange={(e) => setTaskForm({ ...taskForm, date: e.target.value })}
            />
            <select
              value={taskForm.subject}
              onChange={(e) => setTaskForm({ ...taskForm, subject: e.target.value })}
            >
              <option value="">-- اختر مادة --</option>
              {subjects.map((s, idx) => (
                <option key={idx} value={s}>
                  {s}
                </option>
              ))}
            </select>
            <input
              type="number"
              placeholder="Time (minutes)"
              value={taskForm.time}
              onChange={(e) => setTaskForm({ ...taskForm, time: e.target.value })}
            />
            <button onClick={addTask}>Add Task</button>
          </div>
          <div className="task-list">
            {tasks.length === 0 && <p>لا توجد مهام حالياً</p>}
            {tasks.map((t, idx) => (
              <div key={idx} className="task-item">
                <div>
                  <strong>{t.name}</strong> - {t.subject  "بدون مادة"} - {t.date  "No date"}{" "}
                  {t.time ? (${t.time} min) : ""}
                </div>
                <button onClick={() => removeTask(idx)}>✕</button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
import React, { useState, useEffect } from 'react';
import { IconChecklist, IconTrash } from './Icons';

const ProductivityView = () => {
  const [tasks, setTasks] = useState([]);
  const [notes, setNotes] = useState([]);
  const [newTaskText, setNewTaskText] = useState("");
  const [newTaskPriority, setNewTaskPriority] = useState("medium");
  const [newNoteText, setNewNoteText] = useState("");

  const fetchProductivity = async () => {
    try {
      const [tasksRes, notesRes] = await Promise.all([
        fetch("http://localhost:8000/api/tasks"),
        fetch("http://localhost:8000/api/notes")
      ]);
      const tasksData = await tasksRes.json();
      const notesData = await notesRes.json();
      setTasks(tasksData);
      setNotes(notesData);
    } catch (e) {
      console.log("Error loading productivity data:", e);
    }
  };

  useEffect(() => {
    fetchProductivity();
  }, []);

  const handleAddTask = async (e) => {
    e.preventDefault();
    if (!newTaskText.trim()) return;
    try {
      const res = await fetch("http://localhost:8000/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: newTaskText.trim(), priority: newTaskPriority })
      });
      const data = await res.json();
      setTasks(data.tasks);
      setNewTaskText("");
    } catch (e) {
      console.log("Error adding task:", e);
    }
  };

  const handleToggleTask = async (taskId) => {
    try {
      const res = await fetch("http://localhost:8000/api/tasks/toggle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task_id: taskId })
      });
      const data = await res.json();
      setTasks(data.tasks);
    } catch (e) {
      console.log("Error toggling task:", e);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      const res = await fetch(`http://localhost:8000/api/tasks/${taskId}`, { method: "DELETE" });
      const data = await res.json();
      setTasks(data.tasks);
    } catch (e) {
      console.log("Error deleting task:", e);
    }
  };

  const handleAddNote = async (e) => {
    e.preventDefault();
    if (!newNoteText.trim()) return;
    try {
      const res = await fetch("http://localhost:8000/api/notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: newNoteText.trim() })
      });
      const data = await res.json();
      setNotes(data.notes);
      setNewNoteText("");
    } catch (e) {
      console.log("Error adding note:", e);
    }
  };

  const handleDeleteNote = async (noteId) => {
    try {
      const res = await fetch(`http://localhost:8000/api/notes/${noteId}`, { method: "DELETE" });
      const data = await res.json();
      setNotes(data.notes);
    } catch (e) {
      console.log("Error deleting note:", e);
    }
  };

  return (
    <div className="productivity-view">
      {/* Tasks Column */}
      <div className="panel-card">
        <div className="panel-header">
          <span className="panel-title">
            <IconChecklist size={14} />
            Task Checklist ({tasks.filter(t => t.status === 'pending').length} Pending)
          </span>
        </div>

        <form onSubmit={handleAddTask} style={{ padding: '12px', display: 'flex', gap: '6px', borderBottom: '1px solid var(--border-subtle)' }}>
          <input
            type="text"
            className="form-input"
            style={{ flex: 1 }}
            placeholder="Add new task..."
            value={newTaskText}
            onChange={(e) => setNewTaskText(e.target.value)}
          />
          <select
            className="form-input"
            value={newTaskPriority}
            onChange={(e) => setNewTaskPriority(e.target.value)}
            style={{ width: '85px', fontSize: '11px' }}
          >
            <option value="low">Low</option>
            <option value="medium">Med</option>
            <option value="high">High</option>
          </select>
          <button type="submit" className="pill-btn active">Add</button>
        </form>

        <div style={{ flex: 1, overflowY: 'auto', padding: '12px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {tasks.length === 0 ? (
            <div style={{ textAlign: 'center', color: 'var(--text-dim)', padding: '30px' }}>No active tasks.</div>
          ) : (
            tasks.map(task => {
              const isDone = task.status === 'completed';
              return (
                <div key={task.id || task.content} className={`task-item ${isDone ? 'completed' : ''}`}>
                  <div className="task-content">
                    <input
                      type="checkbox"
                      checked={isDone}
                      onChange={() => handleToggleTask(task.id || task.content)}
                      style={{ cursor: 'pointer', accentColor: 'var(--accent-cyan)' }}
                    />
                    <span>{task.content}</span>
                    <span className={`priority-tag ${task.priority || 'medium'}`}>
                      {task.priority || 'medium'}
                    </span>
                  </div>
                  <button
                    className="action-btn"
                    style={{ width: '24px', height: '24px' }}
                    onClick={() => handleDeleteTask(task.id || task.content)}
                  >
                    <IconTrash size={12} />
                  </button>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Smart Notes Column */}
      <div className="panel-card">
        <div className="panel-header">
          <span className="panel-title">Smart Notes & Memos</span>
        </div>

        <form onSubmit={handleAddNote} style={{ padding: '12px', display: 'flex', gap: '6px', borderBottom: '1px solid var(--border-subtle)' }}>
          <input
            type="text"
            className="form-input"
            style={{ flex: 1 }}
            placeholder="Save a note or memo..."
            value={newNoteText}
            onChange={(e) => setNewNoteText(e.target.value)}
          />
          <button type="submit" className="pill-btn active">Save</button>
        </form>

        <div style={{ flex: 1, overflowY: 'auto', padding: '12px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {notes.length === 0 ? (
            <div style={{ textAlign: 'center', color: 'var(--text-dim)', padding: '30px' }}>No notes saved.</div>
          ) : (
            notes.map(note => (
              <div key={note.id || note.content} className="task-item">
                <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  <div style={{ fontSize: '13px' }}>{note.content}</div>
                  <span style={{ fontSize: '10px', fontFamily: 'var(--font-mono)', color: 'var(--text-dim)' }}>
                    {note.created_at ? new Date(note.created_at).toLocaleDateString() : 'Recent'}
                  </span>
                </div>
                <button
                  className="action-btn"
                  style={{ width: '24px', height: '24px' }}
                  onClick={() => handleDeleteNote(note.id)}
                >
                  <IconTrash size={12} />
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductivityView;

import { useState, useEffect } from 'react';

function App() {
  const [tasks, setTasks] = useState(() => {
    const savedTasks = localStorage.getItem('tasks');
    return savedTasks ? JSON.parse(savedTasks) : [];
  });
  
  const [inputValue, setInputValue] = useState('');
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [editingTask, setEditingTask] = useState(null);
  const [editValue, setEditValue] = useState('');
  const [taskPriority, setTaskPriority] = useState('medium');
  const [dueDate, setDueDate] = useState('');
  const [category, setCategory] = useState('personal');
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true';
  });
  const [sortBy, setSortBy] = useState('newest');
  const [viewingTask, setViewingTask] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);

  useEffect(() => {
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }, [tasks]);

  useEffect(() => {
    localStorage.setItem('darkMode', darkMode.toString());
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [darkMode]);

  const addTask = () => {
    if (inputValue.trim() === '') {
      alert('Please enter a task! 📝');
      return;
    }

    const newTask = {
      id: Date.now(),
      text: inputValue.trim(),
      completed: false,
      priority: taskPriority,
      dueDate: dueDate || null,
      category: category,
      createdAt: new Date().toISOString()
    };

    setTasks([newTask, ...tasks]);
    setInputValue('');
    setTaskPriority('medium');
    setDueDate('');
    setCategory('personal');
    setShowAddForm(false);
  };

  const deleteTask = (taskId) => {
    const updatedTasks = tasks.filter(task => task.id !== taskId);
    setTasks(updatedTasks);
  };

  const toggleComplete = (taskId) => {
    const updatedTasks = tasks.map(task => 
      task.id === taskId ? { ...task, completed: !task.completed } : task
    );
    setTasks(updatedTasks);
  };

  const startEditing = (task) => {
    setEditingTask(task);
    setEditValue(task.text);
  };

  const saveEdit = () => {
    if (editValue.trim() === '') {
      alert('Task cannot be empty! ⚠️');
      return;
    }
    
    const updatedTasks = tasks.map(task =>
      task.id === editingTask.id ? { ...task, text: editValue.trim() } : task
    );
    setTasks(updatedTasks);
    setEditingTask(null);
    setEditValue('');
  };

  const cancelEdit = () => {
    setEditingTask(null);
    setEditValue('');
  };

  const clearCompleted = () => {
    if (confirm('Are you sure you want to clear all completed tasks?')) {
      const updatedTasks = tasks.filter(task => !task.completed);
      setTasks(updatedTasks);
    }
  };

  const moveUp = (index) => {
    if (index === 0) return;
    const updatedTasks = [...tasks];
    [updatedTasks[index], updatedTasks[index - 1]] = [updatedTasks[index - 1], updatedTasks[index]];
    setTasks(updatedTasks);
  };

  const moveDown = (index) => {
    if (index === tasks.length - 1) return;
    const updatedTasks = [...tasks];
    [updatedTasks[index], updatedTasks[index + 1]] = [updatedTasks[index + 1], updatedTasks[index]];
    setTasks(updatedTasks);
  };

  const exportTasks = () => {
    const dataStr = JSON.stringify(tasks, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `tasks-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const importTasks = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const importedTasks = JSON.parse(e.target.result);
          setTasks([...tasks, ...importedTasks]);
          alert('Tasks imported successfully! 🎉');
        } catch (error) {
          alert('Error importing tasks. Please check the file format.');
        }
      };
      reader.readAsText(file);
    }
  };

  const deleteTaskWithConfirm = (taskId) => {
    if (confirm('Are you sure you want to delete this task?')) {
      deleteTask(taskId);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      addTask();
    }
  };

  const getPriorityColor = (priority) => {
    switch(priority) {
      case 'high': return '#ff4757';
      case 'medium': return '#ffa502';
      case 'low': return '#2ecc71';
      default: return '#667eea';
    }
  };

  const getCategoryEmoji = (cat) => {
    const emojis = {
      personal: '👤',
      work: '💼',
      shopping: '🛒',
      health: '❤️',
      finance: '💰',
      education: '📚',
      other: '📌'
    };
    return emojis[cat] || '📌';
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  const isOverdue = (task) => {
    if (!task.dueDate || task.completed) return false;
    return new Date(task.dueDate) < new Date();
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    
    if (searchQuery && !task.text.toLowerCase().includes(searchQuery.toLowerCase())) {
      return false;
    }
    
    return true;
  });

  const sortedTasks = [...filteredTasks].sort((a, b) => {
    switch(sortBy) {
      case 'newest': return b.id - a.id;
      case 'oldest': return a.id - b.id;
      case 'priority': 
        const priorityOrder = { high: 0, medium: 1, low: 2 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      case 'dueDate':
        if (!a.dueDate) return 1;
        if (!b.dueDate) return -1;
        return new Date(a.dueDate) - new Date(b.dueDate);
      default: return 0;
    }
  });

  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.completed).length;
  const activeTasks = totalTasks - completedTasks;
  const completionPercentage = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;
  const highPriorityTasks = tasks.filter(t => t.priority === 'high' && !t.completed).length;
  const overdueTasks = tasks.filter(t => isOverdue(t)).length;

  return (
    <div className={`app-container ${darkMode ? 'dark-mode' : ''}`}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px'}}>
        <h1>📝 My Task Manager</h1>
        <button 
          className="theme-toggle-btn"
          onClick={() => setDarkMode(!darkMode)}
          title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        >
          {darkMode ? '☀️' : '🌙'}
        </button>
      </div>
      <p className="subtitle">Stay organized and boost your productivity!</p>
      
      <div className="stats-container">
        <div className="stat-card">
          <div className="stat-number">{totalTasks}</div>
          <div className="stat-label">Total Tasks</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{activeTasks}</div>
          <div className="stat-label">Active</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{completedTasks}</div>
          <div className="stat-label">Completed</div>
        </div>
        <div className="stat-card">
          <div className="stat-number" style={{color: '#ff4757'}}>{highPriorityTasks}</div>
          <div className="stat-label">High Priority</div>
        </div>
        <div className="stat-card">
          <div className="stat-number" style={{color: '#ffa502'}}>{overdueTasks}</div>
          <div className="stat-label">Overdue</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{completionPercentage}%</div>
          <div className="stat-label">Progress</div>
        </div>
      </div>

      <div style={{display: 'flex', gap: '10px', marginBottom: '20px', flexWrap: 'wrap'}}>
        <button className="action-btn secondary-btn" onClick={() => setShowAddForm(!showAddForm)}>
          {showAddForm ? '❌ Cancel' : '➕ Add Task'}
        </button>
        <button className="action-btn secondary-btn" onClick={exportTasks}>
          📤 Export
        </button>
        <label className="action-btn secondary-btn" style={{cursor: 'pointer'}}>
          📥 Import
          <input 
            type="file" 
            accept=".json"
            onChange={importTasks}
            style={{display: 'none'}}
          />
        </label>
        <select 
          className="filter-btn" 
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          style={{marginLeft: 'auto'}}
        >
          <option value="newest">Newest First</option>
          <option value="oldest">Oldest First</option>
          <option value="priority">By Priority</option>
          <option value="dueDate">By Due Date</option>
        </select>
      </div>

      {showAddForm && (
        <div className="enhanced-form">
          <input
            type="text"
            className="task-input"
            placeholder="✨ What needs to be done?"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            autoFocus
          />
          <div style={{display: 'flex', gap: '10px', marginTop: '10px', flexWrap: 'wrap'}}>
            <select 
              value={taskPriority}
              onChange={(e) => setTaskPriority(e.target.value)}
              className="form-select"
            >
              <option value="low">🟢 Low Priority</option>
              <option value="medium">🟡 Medium Priority</option>
              <option value="high">🔴 High Priority</option>
            </select>
            <input
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="form-select"
            />
            <select 
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="form-select"
            >
              <option value="personal">👤 Personal</option>
              <option value="work">💼 Work</option>
              <option value="shopping">🛒 Shopping</option>
              <option value="health">❤️ Health</option>
              <option value="finance">💰 Finance</option>
              <option value="education">📚 Education</option>
              <option value="other">📌 Other</option>
            </select>
            <button className="add-button" onClick={addTask}>
              ➕ Add Task
            </button>
          </div>
        </div>
      )}

      <div className="search-container">
        <input
          type="text"
          className="search-input"
          placeholder="🔍 Search tasks..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      <div className="filters-container">
        <button 
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All ({totalTasks})
        </button>
        <button 
          className={`filter-btn ${filter === 'active' ? 'active' : ''}`}
          onClick={() => setFilter('active')}
        >
          Active ({activeTasks})
        </button>
        <button 
          className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
          onClick={() => setFilter('completed')}
        >
          Completed ({completedTasks})
        </button>
      </div>

      {sortedTasks.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">📋</div>
          <p className="empty-state-text">
            {searchQuery ? 'No tasks match your search!' : 
             filter === 'completed' ? 'No completed tasks yet!' :
             filter === 'active' ? 'No active tasks! Great job!' :
             'No tasks yet! Add your first task above.'}
          </p>
        </div>
      ) : (
        <>
          <ul className="task-list">
            {sortedTasks.map((task, index) => (
              <li 
                key={task.id} 
                className={`task-item ${task.completed ? 'completed' : ''}`}
                style={{borderLeftColor: getPriorityColor(task.priority)}}
              >
                <label className="checkbox-wrapper">
                  <input
                    type="checkbox"
                    className="task-checkbox"
                    checked={task.completed}
                    onChange={() => toggleComplete(task.id)}
                  />
                </label>
                <span className="task-text" onClick={() => setViewingTask(task)} style={{cursor: 'pointer'}}>
                  {task.text}
                  {task.priority === 'high' && !task.completed && <span className="priority-badge high">🔴</span>}
                  {task.priority === 'medium' && !task.completed && <span className="priority-badge medium">🟡</span>}
                  {task.priority === 'low' && !task.completed && <span className="priority-badge low">🟢</span>}
                </span>
                <span className="category-badge">
                  {getCategoryEmoji(task.category)} {task.category}
                </span>
                {task.dueDate && (
                  <span className={`due-date-badge ${isOverdue(task) ? 'overdue' : ''}`}>
                    📅 {formatDate(task.dueDate)}
                  </span>
                )}
                <div className="task-actions">
                  <button 
                    className="action-btn view-btn"
                    onClick={() => setViewingTask(task)}
                    title="View Details"
                  >
                    👁️
                  </button>
                  <button 
                    className="action-btn move-up-btn"
                    onClick={() => moveUp(index)}
                    disabled={index === 0}
                    title="Move Up"
                  >
                    ⬆️
                  </button>
                  <button 
                    className="action-btn move-down-btn"
                    onClick={() => moveDown(index)}
                    disabled={index === sortedTasks.length - 1}
                    title="Move Down"
                  >
                    ⬇️
                  </button>
                  <button 
                    className="action-btn edit-btn"
                    onClick={() => startEditing(task)}
                    title="Edit Task"
                  >
                    ✏️
                  </button>
                  <button 
                    className="action-btn delete-btn"
                    onClick={() => deleteTaskWithConfirm(task.id)}
                    title="Delete Task"
                  >
                    🗑️
                  </button>
                </div>
              </li>
            ))}
          </ul>
          
          <p className="task-count">
            📊 Showing {sortedTasks.length} of {totalTasks} tasks 
            {completionPercentage > 0 && `• ${completionPercentage}% completed`}
          </p>

          {completedTasks > 0 && (
            <button 
              className="clear-completed-btn"
              onClick={clearCompleted}
            >
              🧹 Clear Completed Tasks ({completedTasks})
            </button>
          )}
        </>
      )}

      {viewingTask && (
        <div className="modal-overlay" onClick={() => setViewingTask(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2 className="modal-title">📋 Task Details</h2>
            <div className="task-detail-section">
              <p><strong>Task:</strong> {viewingTask.text}</p>
              <p><strong>Status:</strong> {viewingTask.completed ? '✅ Completed' : '⏳ Active'}</p>
              <p><strong>Priority:</strong> 
                <span style={{color: getPriorityColor(viewingTask.priority), fontWeight: 'bold'}}>
                  {' '}{viewingTask.priority.toUpperCase()}
                </span>
              </p>
              <p><strong>Category:</strong> {getCategoryEmoji(viewingTask.category)} {viewingTask.category}</p>
              {viewingTask.dueDate && (
                <p><strong>Due Date:</strong> 
                  <span className={isOverdue(viewingTask) ? 'overdue-text' : ''}>
                    {' '}{formatDate(viewingTask.dueDate)}
                  </span>
                </p>
              )}
              <p><strong>Created:</strong> {formatDate(viewingTask.createdAt)}</p>
            </div>
            <div className="modal-actions">
              <button className="cancel-btn" onClick={() => setViewingTask(null)}>
                Close
              </button>
              {!viewingTask.completed && (
                <button className="save-btn" onClick={() => {
                  toggleComplete(viewingTask.id);
                  setViewingTask({...viewingTask, completed: true});
                }}>
                  ✅ Mark Complete
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {editingTask && (
        <div className="modal-overlay" onClick={cancelEdit}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2 className="modal-title">✏️ Edit Task</h2>
            <input
              type="text"
              className="modal-input"
              value={editValue}
              onChange={(e) => setEditValue(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && saveEdit()}
              autoFocus
            />
            <div className="modal-actions">
              <button className="cancel-btn" onClick={cancelEdit}>
                Cancel
              </button>
              <button className="save-btn" onClick={saveEdit}>
                💾 Save Changes
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

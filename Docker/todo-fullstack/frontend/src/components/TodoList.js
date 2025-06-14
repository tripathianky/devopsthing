import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function TodoList({ token, onLogout }) {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [error, setError] = useState(null);

  const api = axios.create({
    baseURL: 'http://localhost:5000',
    headers: { Authorization: `Bearer ${token}` }
  });

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const res = await api.get('/todos');
      setTodos(res.data);
    } catch (err) {
      setError('Failed to load todos');
      if (err.response?.status === 401) onLogout();
    }
  };

  const addTodo = async () => {
    if (!newTodo.trim()) return;
    try {
      const res = await api.post('/todos', { title: newTodo });
      setTodos([...todos, res.data]);
      setNewTodo('');
    } catch (err) {
      setError('Failed to add todo');
    }
  };

  const toggleDone = async (id, done) => {
    try {
      await api.put(`/todos/${id}`, { done: !done });
      setTodos(todos.map(t => (t.id === id ? { ...t, done: !done } : t)));
    } catch {
      setError('Failed to update todo');
    }
  };

  const deleteTodo = async (id) => {
    try {
      await api.delete(`/todos/${id}`);
      setTodos(todos.filter(t => t.id !== id));
    } catch {
      setError('Failed to delete todo');
    }
  };

  return (
    <div>
      <h2>Todo List</h2>
      <button onClick={onLogout}>Logout</button>
      {error && <p style={{color: 'red'}}>{error}</p>}
      <input value={newTodo} onChange={e => setNewTodo(e.target.value)} placeholder="New todo" />
      <button onClick={addTodo}>Add</button>
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>
            <input type="checkbox" checked={todo.done} onChange={() => toggleDone(todo.id, todo.done)} />
            {todo.title}
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

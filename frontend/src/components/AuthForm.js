import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const AuthForm = ({ onSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/login', { username, password });
      localStorage.setItem('accessToken', response.data.access_token);
      onSuccess();
      navigate('/profile');
    } catch (err) {
      console.error(err);
      alert('Ошибка авторизации.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="auth-form">
      <input 
        type="text" 
        value={username} 
        onChange={e => setUsername(e.target.value)}
        placeholder="Имя пользователя"
        className="form-input"
      />
      <input 
        type="password" 
        value={password} 
        onChange={e => setPassword(e.target.value)}
        placeholder="Пароль"
        className="form-input"
      />
      <button type="submit" className="form-button">Войти</button>
    </form>
  );
};

export default AuthForm;
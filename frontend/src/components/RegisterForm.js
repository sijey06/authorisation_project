import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const RegisterForm = ({ onSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      await axios.post('/api/register', { username, password });
      onSuccess();
      navigate('/'); 
    } catch (err) {
      if (err.response?.status === 400) {
        setErrorMessage(err.response.data.detail);
      } else {
        console.error(err);
      }
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
      <button type="submit" className="form-button">Зарегистрироваться</button>
    </form>
  );
};

export default RegisterForm;
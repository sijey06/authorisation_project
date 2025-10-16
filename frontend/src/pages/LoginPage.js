import React from 'react';
import { useNavigate } from 'react-router-dom';
import AuthForm from '../components/AuthForm';

const LoginPage = () => {
  const navigate = useNavigate();
  const handleSuccess = () => {
    navigate('/');
  };

  return (
    <div className="page-container">
      <div className="form-container">
        <h1>Форма входа</h1>
        <AuthForm onSuccess={handleSuccess}/>
        <div className="buttons-group">
          <button className="auth-button secondary" onClick={() => navigate('/register')}>Зарегистрироваться</button>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
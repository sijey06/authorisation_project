import React from 'react';
import RegisterForm from '../components/RegisterForm';

const RegisterPage = () => {
  const handleSuccess = () => alert('Вы зарегистрированы!');

  return (
    <div className="page-container">
      <div className="form-container">
        <h1>Форма регистрации</h1>
        <RegisterForm onSuccess={handleSuccess}/>
      </div>
    </div>
  );
};

export default RegisterPage;
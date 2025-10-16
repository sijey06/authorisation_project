import React from 'react';
import axios from 'axios';

const LogoutButton = () => {
  const handleClick = async () => {
    try {
      const token = localStorage.getItem('accessToken');

      if (!token) throw new Error('Нет токена для выхода');

      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      await axios.post('/api/logout', {}, config);
      localStorage.removeItem('accessToken');
      window.location.href = '/'
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <button className="logout-button" onClick={handleClick}>
      Выйти
    </button>
  );
};

export default LogoutButton;
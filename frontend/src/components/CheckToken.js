import React, { useEffect, useState } from 'react';
import axios from 'axios';

const CheckToken = () => {
  const [validity, setValidity] = useState(null);
  const [username, setUsername] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        
        if (!token) throw new Error('Нет токена');

        const config = {
          headers: {
            Authorization: `Bearer ${token}`
          }
        };

        const response = await axios.get('/api/me', config);
        setValidity(response.data.isValid);
        setUsername(response.data.username);
      } catch (err) {
        console.error(err);
        setValidity(false);
      }
    };

    fetchData();
  }, []);

  let message;
  if (validity === null) {
    message = <span className="loading-indicator">Проверка токена...</span>;
  } else if (validity) {
    message = (
      <div>
        <span className="check-token-message">{`Привет, ${username}!`}</span>
        <br />
        <span className="check-token-message">Ваш токен действителен</span>
      </div>
    );
  } else {
    message = <span className="check-token-message invalid">Ваш токен недействителен</span>;
  }

  return <p>{message}</p>;
};

export default CheckToken;
import React from 'react';
import CheckToken from '../components/CheckToken';
import LogoutButton from '../components/LogoutButton';

const ProfilePage = () => {
  return (
    <div className="page-container">
      <div className="form-container profile-page">
        <h1>Страница профиля</h1>
        <CheckToken />
        <LogoutButton />
      </div>
    </div>
  );
};

export default ProfilePage;
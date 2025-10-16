import axios from 'axios';

export const loginUser = async credentials => {
  const res = await axios.post('http://localhost:8000/api/login', credentials);
  return res.data.access_token;
};

export const registerUser = async data => {
  await axios.post('http://localhost:8000/api/register', data);
};

export const checkToken = async () => {
  const res = await axios.get('http://localhost:8000/api/me');
  return res.data.isValid;
};

export const logoutUser = async () => {
  await axios.post('http://localhost:8000/api/logout');
};
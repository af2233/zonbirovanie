import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

import './Register.css';
import waveImage from '../../assets/wave-log-in.svg';
import logoImage from '../../assets/logo-log-in.svg';
import { fetchWithRefresh } from '../Utils.jsx';


const Register = () => {
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState('');

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });

  const [error, setError] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(false);
    setErrorMessage('');

    const { username, email, password } = formData;

    if (!username || !email || !password) {
      setError(true);
      return;
    }

    try {
      const res = await fetchWithRefresh('http://localhost:8000/api/v1/auth/users/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
      });

      if (res.ok) {
        navigate('/login');
        return;
      }

      const data = await res.json();
      const messages = Object.values(data).flat().join(' ');
      setError(true);
      setErrorMessage(messages || 'Ошибка регистрации');
    } catch (err) {
      setError(true);
      setErrorMessage('Ошибка подключения к серверу'); 
    }
  };

  return (
    <div className="register-container">
      <div className="wave-container">
        <img src={waveImage} alt="wave background" />
      </div>

      <div className="logo-container">
        <img src={logoImage} alt="logo" />
      </div>

      <div className="wrapper">
        <form onSubmit={handleSubmit}>
          <h1>Регистрация</h1>
          <div className="divider"></div>

          <div className="input-box">
            <label htmlFor="username">Имя</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-box">
            <label htmlFor="email">Почта</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-box">
            <label htmlFor="password">Пароль</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
            {error && (
              <span className="error-message">
                {errorMessage || 'Неверно введены данные'}
              </span>
            )}
          </div>

          <button type="submit" className="btn">
            Продолжить
          </button>
        </form>
      </div>

      <div className="register-link">
        <p>Уже есть аккаунт? <Link to="/login" style={{ fontSize: '12px', fontWeight: 500 }}>Войти</Link></p>
      </div>
    </div>
  );
};

export default Register;

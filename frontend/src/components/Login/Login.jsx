import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import './Login.css';
import waveImage from '../../images/wave-log-in.svg';
import logoImage from '../../images/logo-log-in.svg';

const Login = () => {
    const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(false);

    if (!username || !password) {
      setError(true);
      return;
    }

    try {
      const res = await fetch('http://localhost:8000/api/v1/auth/jwt/create/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await res.json();

      if (res.ok) {
        localStorage.setItem('access', data.access);
        localStorage.setItem('refresh', data.refresh);
        navigate('/loading');
      } else {
        setError(true);
      }
    } catch (err) {
      setError(true);
    }
  };

  return (
    <div className="login-container">
      <div className="wave-container">
        <img src={waveImage} alt="wave background" />
      </div>

      <div className="logo-container">
        <img src={logoImage} alt="logo" />
      </div>

      <div className="wrapper">
        <form onSubmit={handleSubmit}>
          <h1>Вход в аккаунт</h1>
          <div className="divider"></div>

          <div className="input-box">
            <label htmlFor="username">Имя</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="input-box">
            <label htmlFor="password">Пароль</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {error && (
              <span className="error-message">
                Неверно введены имя пользователя или пароль
              </span>
            )}
          </div>

          <button type="submit" className="btn-login">
            Продолжить
          </button>
        </form>
      </div>

      <div className="register-link">
        <p>Нет аккаунта? <Link to="/register" style={{ fontSize: '12px', fontWeight: 500 }}>Зарегистрироваться</Link></p>
      </div>
    </div>
  );
};

export default Login;
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Login.css';
import waveImage from '../../images/wave-log-in.svg';
import logoImage from '../../images/logo-log-in.svg';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!email || !password) {
      setError(true);
      return;
    }
    console.log('Вход:', { email, password });
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
            <label htmlFor="email">Почта</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
                Неверно введена почта или пароль
              </span>
            )}
          </div>

          <button type="submit" className="btn" onClick={() => window.location.href='/loading'}>
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
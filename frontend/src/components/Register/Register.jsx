import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Register.css';
import waveImage from '../../images/wave-log-in.svg';
import logoImage from '../../images/logo-log-in.svg';

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
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
    setError('');
    const res = await fetch('${process.env.REGISTER_URL}', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, username, password }),
    });
    const data = await res.json();
    if (res.ok) {
        navigate('/login');
    } else {
        setError('Ошибка регистрации');
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
            <label htmlFor="name">Имя</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
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
                Неверно введены данные
              </span>
            )}
          </div>

          <button type="submit" className="btn" onClick={() => window.location.href='/loading'}>
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
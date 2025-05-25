import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

import './Home.css';
import rectangleImage from '../../assets/rectangle.png';
import logoImage from '../../assets/logo.svg';
import waveImage from '../../assets/wave.svg';
import { fetchWithRefresh } from '../Utils.jsx';
import UserInfo from '../Utils.jsx';


const Home = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('access');
      if (!token) return;

      try {
        const res = await fetchWithRefresh('http://localhost:8000/api/v1/auth/users/me/', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        if (res.ok) {
          const data = await res.json();
          setUsername(data.username);
        }
      } catch (err) {
        console.error('Ошибка получения пользователя', err);
      }
    };

    fetchUser();
  }, []);

  const handleLogout = async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      localStorage.clear();
      navigate('/');
      window.location.reload();
      return;
    }

    try {
      const res = await fetchWithRefresh('http://localhost:8000/api/v1/auth/logout/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      if (res.status === 205) {
        localStorage.clear();
        navigate('/');
        window.location.reload();
      } else {
        console.error('Ошибка выхода');
      }
    } catch (err) {
      console.error('Ошибка сети при выходе', err);
    }
  };

  return (
    <div className="home-container">
      {/* HEADER */}
      <header className="header">
        <img src={rectangleImage} alt="" className="head-rectangle"/>
        <img src={logoImage} alt="Logo" className="logo"/>
        <UserInfo username={username} handleLogout={handleLogout}/>
      </header>

      {/* MAIN */}
      <main>
        <div className="container">
          <div className="wave">
            <img src={waveImage} alt="Wave" />
          </div>
          <div className="main-content">
            <div className="main-left">
              <h1>
                <span className="white">АВТОМАТИЗИРОВАННЫЙ</span><br/>
                <span className="blue">АНАЛИЗ </span>
                <span className="white">МОРСКИХ</span><br/>
                <span className="blue">ЗАГРЯЗНЕНИЙ</span>
              </h1>
              <p className="subtitle">
                Наш сервис помогает выявлять нефтяные разливы<br/>
                с высокой точностью. Используйте современные<br/>
                технологии для мониторинга экологической<br/>
                безопасности водных ресурсов.
              </p>
              <div className="main-content-button">
                <Link to="/loading"><span className="white">Начать работу прямо сейчас!</span></Link>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* FOOTER */}
      <footer className="copyright">
        <p>© 2025 zonbirovanie</p>
      </footer>
    </div>
  );
};

export default Home;

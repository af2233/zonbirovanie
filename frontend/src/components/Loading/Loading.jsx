import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

import './Loading.css';
import logo from "../../assets/logo.svg";
import userIcon from "../../assets/user-icon.svg";
import loadingCloud from "../../assets/loading-cloud.svg";
import exitIcon from "../../assets/logout.png";
import { fetchWithRefresh } from '../Utils.jsx';
import UserInfo from '../Utils.jsx';


const Loading = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

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
    <div className="loading-container">
      {/* Header */}
      <header className="loading-header">
        <div className="header-content">
          <Link to="/">
            <img
              src={logo}
              alt="Zonbirovanie"
              className="logo"
              style={{ cursor: 'pointer' }}
            />
          </Link>
          <UserInfo username={username} handleLogout={handleLogout}/>
        </div>
      </header>

      {/* Main Content */}
      <main className="loading-main">

        <div className="content-wrapper">
          <h1>Загрузите снимок для анализа нефтяных загрязнений</h1>
          <p className="subtitle">Наша система обработает изображение и выявит возможные нефтяные разливы</p>

          <div className="upload-area">
            <label htmlFor="file-upload" className="upload-label">
              <img
                src={loadingCloud}
                alt="Upload icon"
                className="upload-icon"
              />
              <span>Выберите изображение</span>
            </label>
            <input
              id="file-upload"
              type="file"
              className="file-input"
              onChange={(e) => setSelectedFile(e.target.files[0])}
            />
          </div>

          <button className="action-button">Начать анализ</button>
        </div>
      </main>

      {/* Footer */}
      <footer className="copyright">
        <p>© 2025 zonbirovanie</p>
      </footer>
    </div>
  );
};

export default Loading;

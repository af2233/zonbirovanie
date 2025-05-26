import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import './Home.css';
import rectangleImage from '../../assets/rectangle.png';
import logoImage from '../../assets/logo.svg';
import waveImage from '../../assets/wave.svg';
import { fetchUser } from '../Utils.jsx';
import UserInfo from '../Utils.jsx';


const Home = () => {
  const [username, setUsername] = useState('');

  useEffect(() => {
    fetchUser(setUsername);
  }, []);

  return (
    <div className="home-container">

      {/* HEADER */}
      <header className="header">
        <img src={rectangleImage} alt="" className="head-rectangle"/>
        <img src={logoImage} alt="Logo" className="logo"/>
        <UserInfo username={username}/>
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

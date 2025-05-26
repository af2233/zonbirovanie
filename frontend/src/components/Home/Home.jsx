import './Home.css';
import { useEffect, useState } from 'react';
import rectangleImage from '../../images/rectangle.png';
import logoImage from '../../images/logo.svg';
import waveImage from '../../images/wave.svg';
import { Link } from 'react-router-dom';
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
        <img src={rectangleImage} alt="" className="head-rectangle" />
        <img src={logoImage} alt="Logo" className="logo" />
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
                <span className="white">Автоматизированный </span><br />
                <span className="blue">анализ </span>
                <span className="white">морских </span><br />
                <span className="blue">загрязнений</span>
              </h1>
              <p>
                Наш сервис помогает выявлять нефтяные разливы с <br />
                высокой точностью. Используйте современные <br />
                технологии для мониторинга экологической <br />
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
      <footer>
        <div className="copyright">
          <span className="white">@ 2025 zonbirovanie</span>
        </div>
      </footer>
    </div>
  );
};

export default Home;
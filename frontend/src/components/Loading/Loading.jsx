import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import './Loading.css';
import logo from "../../assets/logo.svg";
import loadingCloud from "../../assets/loading-cloud.svg";
import folderIcon from "../../assets/folder.png";
import { fetchUser } from '../Utils.jsx';
import UserInfo from '../Utils.jsx';


const Loading = () => {
  const [username, setUsername] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  useEffect(() => {
    fetchUser(setUsername);
  }, []);

  return (
    <div className="loading-container">

      {/* HEADER */}
      <header className="loading-header">
        <div className="header-content">
          <Link to="/">
            <img
              src={logo}
              alt="Zonbirovanie"
              className="logo"
            />
          </Link>
          <UserInfo username={username}/>
        </div>
      </header>

      {/* MAIN */}
      <main className="loading-main">

        <div className="content-wrapper">
          <h1>Загрузите снимок для анализа нефтяных загрязнений</h1>
          <p className="subtitle">Наша система обработает изображение и выявит возможные нефтяные разливы</p>

          {!selectedFile ? (
            <div className="upload-area">
              <label htmlFor="file-upload" className="upload-label">
                <img
                  src={loadingCloud}
                  alt="Upload icon"
                  className="upload-icon"
                />
                <span>Выберите файл</span>
              </label>
              <input
                id="file-upload"
                type="file"
                className="file-input"
                onChange={(e) => setSelectedFile(e.target.files[0])}
              />
            </div>
          ) : (
            <div className="file-info">
              <img src={folderIcon} alt="File icon" className="file-icon" />
              <span className="file-name">{selectedFile.name}</span>
            </div>
          )}
          <button className="action-button">Начать анализ</button>
        </div>
      </main>

      {/* FOOTER */}
      <footer className="copyright">
        <p>© 2025 zonbirovanie</p>
      </footer>

    </div>
  );
};

export default Loading;

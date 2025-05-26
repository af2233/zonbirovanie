import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';

import './Loading.css';

import rectangleImage from '../../images/rectangle.png';
import userIcon from '../../images/user-icon.svg';
import loadingCloud from '../../images/loading-cloud.svg';
import folderIcon from '../../images/folder.png';
import logo from '../../images/logo.svg';
import eclipse from '../../images/ellipse.png';

import { fetchUser } from '../Utils.jsx';
import UserInfo from '../Utils.jsx';

const Loading = () => {
  const [username, setUsername] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isProcessed, setIsProcessed] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState('');
  const downloadRef = useRef(null);

  useEffect(() => {
    fetchUser(setUsername);
  }, []);

  const handleStartAnalysis = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    setIsProcessed(false);
    setDownloadUrl('');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:4000/process/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Ошибка при получении файла');
      }

      // Получить бинарные данные
      const blob = await response.blob();

      // Создать ссылку на скачивание
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url);

      setIsProcessing(false);
      setIsProcessed(true);

      setTimeout(() => {
        downloadRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 300);

    } catch (error) {
      console.error(error);
      setIsProcessing(false);
    }
  };
  return (
    <div className="home-container">
      {/* HEADER */}
      <header className="header">
        <img src={rectangleImage} alt="" className="head-rectangle" />
        <div className="header-content">
          <Link to="/">
            <img src={logo} alt="Zonbirovanie" className="logo"/>
          </Link>
          <UserInfo username={username} />
        </div>
      </header>

      {/* MAIN */}
      <main className="loading-main">
        <div className="content-wrapper">
          <div className="main-caption">
            <h1><span className="white">Загрузите снимок для анализа нефтяных<br />загрязнений</span></h1>
            <p>Наша система обработает изображение и выявит возможные нефтяные разливы</p>
          </div>

          {!selectedFile ? (
            <div className="upload-area">
              <label htmlFor="file-upload" className="upload-label">
                <img src={loadingCloud} alt="Upload icon" className="upload-icon" />
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

          <div className="action-button">
            <button className="white start" onClick={handleStartAnalysis} disabled={isProcessing}>
              {isProcessing ? 'Обработка...' : 'Начать анализ'}
            </button>
          </div>
        </div>

        {isProcessed && downloadUrl && (
          <div className="processing-completed" ref={downloadRef}>
            <div className="text-completed">
              <p><span className="white">Обработка завершена. Ваш архив<br />готов к скачиванию!</span></p>
              <img src={eclipse} alt="" className="circle" />
            </div>

            <div className="download-button">
              <span className="white">
                <a href={downloadUrl} download="results.zip" className="download">
                  Скачать
                </a>
              </span>
            </div>
          </div>
        )}
      </main>

      {/* FOOTER */}
      <footer className="loading-footer">
        <div className="copyright">
          <span className="white">@ 2025 zonbirovanie</span>
        </div>
      </footer>
    </div>
  );
};

export default Loading;

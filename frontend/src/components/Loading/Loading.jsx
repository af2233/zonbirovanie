import React from 'react';
import './Loading.css';

const Loading = () => {
  return (
    <div className="loading-container">
      {/* Header */}
      <header className="loading-header">
        <div className="header-content">
          <img
            src="../../images/logo.svg"
            alt="Zonbirovanie"
            className="logo"
          />
          <div className="user-info">
            <span className="user-name">Виктория</span>
            <img
              src="../../images/user-icon.svg"
              alt="User"
              className="user-icon"
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="loading-main">
        <div className="wave-bg">
          <img
            src="../../images/wave-loading.svg"
            alt="Wave background"
          />
        </div>

        <div className="content-wrapper">
          <h1>Загрузите снимок для анализа нефтяных загрязнений</h1>
          <p className="subtitle">Наша система обработает изображение и выявит возможные нефтяные разливы</p>

          <div className="upload-area">
            <label htmlFor="file-upload" className="upload-label">
              <img
                src="https://raw.githubusercontent.com/AnnaYurch/fund_alg/main/loading-cloud.svg"
                alt="Upload icon"
                className="upload-icon"
              />
              <span>Выберите изображение</span>
            </label>
            <input id="file-upload" type="file" className="file-input" />
          </div>

          <button className="action-button">Начать анализ</button>
        </div>
      </main>

      {/* Footer */}
      <footer className="loading-footer">
        <p>© 2025 zonbirovanie</p>
      </footer>
    </div>
  );
};

export default Loading;
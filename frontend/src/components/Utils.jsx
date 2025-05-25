import { Link } from 'react-router-dom';

import userIcon from '../assets/user-icon.svg';
import logoutIcon from '../assets/logout.png';




const UserInfo = ({ username, handleLogout }) => {
  return (
    <div className="user-info">
      {username ? (
        <>
          <span className="user-name">{username}</span>
          <img src={userIcon} alt="User" className="user-icon" />
          <img
            src={logoutIcon}
            alt="Logout"
            className="logout-icon"
            onClick={handleLogout}
            style={{ cursor: 'pointer' }}
          />
        </>
      ) : (
        <nav className="nav">
          <Link to="/login" className="btn btn-blue">Вход</Link>
          <Link to="/register" className="btn btn-purple">Регистрация</Link>
        </nav>
      )}
    </div>
  );
};




async function fetchWithRefresh(url, options) {
  let access = localStorage.getItem('access');

  let res = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${access}`
    }
  });

  if (res.status === 401) { // access токен просрочен
    const refresh = localStorage.getItem('refresh');
    const refreshRes = await fetch('http://localhost:8000/api/v1/auth/jwt/refresh/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh })
    });

    if (refreshRes.ok) {
      const data = await refreshRes.json();
      localStorage.setItem('access', data.access);

      // Повторяем исходный запрос с новым access токеном
      res = await fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          'Authorization': `Bearer ${data.access}`
        }
      });
    } else {
      // refresh токен просрочен — выходим
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      window.location.href = '/login';
      return;
    }
  }

  return res;
}




export default UserInfo;
export { fetchWithRefresh }

import { Link } from 'react-router-dom';

import userIcon from '../images/user-icon.svg';
import logoutIcon from '../images/logout.png';




export async function fetchWithRefresh(url, options) {
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
      // refresh токен просрочен - выходим
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      window.location.href = '/login'; // page reload
      return;
    }
  }

  return res;
}




export async function handleLogout() {
  const refreshToken = localStorage.getItem('refreshToken');
  if (!refreshToken) {
    localStorage.clear();
    window.location.href = '/'; // page reload
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
      window.location.href = '/'; // page reload
    } else {
      console.error('Ошибка выхода');
    }
  } catch (err) {
    console.error('Ошибка сети при выходе', err);
  }
}




export async function fetchUser(setUsername) {
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
}




function UserInfo({ username }) {
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
}




export default UserInfo;

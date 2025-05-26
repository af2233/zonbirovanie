import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';

import Home from './components/Home/Home';
import Login from './components/Login/Login';
import Register from './components/Register/Register';
import Loading from './components/Loading/Loading';


function AppWrapper() {
  const location = useLocation();

  useEffect(() => {
    // Добавляем класс, если путь = "/"
    if (location.pathname === "/") {
      document.body.classList.add("body-home");
    } else {
      document.body.classList.remove("body-home");
    }
  }, [location]);

  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/loading" element={<Loading />} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AppWrapper />
    </Router>
  );
}

export default App;

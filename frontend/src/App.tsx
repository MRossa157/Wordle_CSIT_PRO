import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import  Popup from "./components/Popup"

const App: React.FC = () => {
  const [login, setLogin] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [loginDirty, setLoginDirty] = useState<boolean>(false);
  const [passwordDirty, setPasswordDirty] = useState<boolean>(false);
  const [passwordError, setPasswordError] = useState<string>("");
  const [formValid, setFormValid] = useState<boolean>(false);
  const [popupMessage, setPopupMessage] = useState<string | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);

  const navigate = useNavigate();

  useEffect(() => {
    setFormValid(!passwordError && login.length > 0);
  }, [passwordError, login]);

  const showPopup = (message: string) => {
    setPopupMessage(message);
    setTimeout(() => setPopupMessage(null), 3000);
  };

  const closePopup = () => {
    setPopupMessage(null);
  };

  const loginHandler = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLogin(e.target.value);
  };

  const passwordHandler = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
    if (e.target.value.length < 8 || e.target.value.length > 12) {
      setPopupMessage("Пароль должен быть длиной от 8 до 12 символов");
      if (!e.target.value) {
        setPopupMessage("Пароль не может быть пустым");
      }
    } else {
      setPopupMessage("");
    }
  };

  const blurHandler = (e: React.FocusEvent<HTMLInputElement>) => {
    switch (e.target.name) {
      case "login":
        setLoginDirty(true);
        break;
      case "password":
        setPasswordDirty(true);
        break;
      default:
        break;
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formValid) {
      showPopup("Заполните форму корректно");
      return;
    }

    const userData = {
      username: login,
      password: password,
    };

    try {
      const response = await fetch("http://localhost:5002/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
        credentials: "include",
      });

      if (response.ok) {
        navigate("/");
      } else {
        const errorData = await response.json();
        showPopup(errorData.message || "Ошибка авторизации");
      }
    } catch (error) {
      console.error("Ошибка при отправке запроса:", error);
      setApiError("Ошибка при соединении с сервером");
    }
  };

  return (
    <div className="app">
    <div className="loginForm">
      <p className="loginForm-title">Авторизация</p>

      <input
        onChange={loginHandler}
        value={login}
        onBlur={blurHandler}
        name="login"
        type="text"
        placeholder="Введите логин..."
        className="loginForm-input"
      />
      <input
        onChange={passwordHandler}
        value={password}
        onBlur={blurHandler}
        name="password"
        type="password"
        placeholder="Введите пароль..."
        className="loginForm-input"
      />

      {passwordDirty && passwordError && (
        <div className="loginForm-error">{passwordError}</div>
      )}
      {apiError && <div className="loginForm-error">{apiError}</div>}

      <button
        className="home-button"
        disabled={!formValid}
        onClick={handleLogin}
        type="submit"
      >
        Вход
      </button>
      <button
        className="home-button"
        onClick={() => navigate("/registration")}
      >
        Зарегистрироваться
      </button>
    </div>

    {popupMessage && <Popup message={popupMessage} onClose={closePopup} duration={3000} />}
  </div>
  );
};

export default App;

import "../App.css";
import React, { useState, useEffect, ChangeEvent, FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import Popup from "./Popup";

const Register: React.FC = () => {
  const [login, setLogin] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');
  const [passwordError, setPasswordError] = useState<string>('');
  const [formValid, setFormValid] = useState<boolean>(false);
  const [popupMessage, setPopupMessage] = useState<string>('');

  const navigate = useNavigate();

  useEffect(() => {
    if (password && confirmPassword && password !== confirmPassword) {
      showPopup('Пароли не совпадают');
      setFormValid(false);
    } else if (password.length < 8 || password.length > 12) {
      showPopup('Пароль должен быть длиннее 8 и меньше 12 символов');
      setFormValid(false);
    } else {
      showPopup('');
      setFormValid(true);
    }
  }, [password, confirmPassword]);

  const showPopup = (message: string) => {
    setPopupMessage(message);
  };

  const closePopup = () => {
    setPopupMessage('');
  };

  const loginHandler = (e: ChangeEvent<HTMLInputElement>) => {
    setLogin(e.target.value);
  };
  const passwordHandler = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
    if (e.target.value.length < 8 || e.target.value.length > 12) {
      setPopupMessage("Пароль должен быть длиной от 8 до 12 символов");
    } else {
      setPopupMessage("");
    }
  };
  
  const confirmPasswordHandler = (e: React.ChangeEvent<HTMLInputElement>) => {
    setConfirmPassword(e.target.value);
    if (e.target.value !== password && e.target.value.length > 0) {
      setPopupMessage("Пароли не совпадают");
    } else {
      setPopupMessage("");
    }
  };

  const handleRegister = async (e: FormEvent) => {
    e.preventDefault();
    if (!formValid) {
      showPopup('Заполните форму корректно');
      return;
    }

    const userData = {
      username: login,
      password,
    };

    try {
      const response = await fetch('http://localhost:5002/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
        credentials: 'include',
      });

      if (response.status === 201) {
        showPopup('Пользователь успешно зарегистрирован!');
        setTimeout(() => navigate('/'), 3000);
      } else {
        const errorData = await response.json();
        showPopup(errorData.message || 'Пользователь с таким именем уже существует');
      }
    } catch (error) {
      console.error('Ошибка при отправке запроса:', error);
      showPopup('Ошибка при соединении с сервером');
    }
  };

  return (
    <div className="app">
      <div className="registerForm">
        <p className="registerForm-title">Регистрация</p>
        <input
          onChange={loginHandler}
          value={login}
          name="login"
          type="text"
          placeholder="Введите логин..."
          className="registerForm-input"
        />
        <input
          onChange={passwordHandler}
          value={password}
          name="password"
          type="password"
          placeholder="Введите пароль..."
          className="registerForm-input"
        />
        <input
          onChange={confirmPasswordHandler}
          value={confirmPassword}
          name="confirmPassword"
          type="password"
          placeholder="Подтвердите пароль..."
          className="registerForm-input"
        />

        {passwordError && <div className="registerForm-error">{passwordError}</div>}

        <button
          className="home-button"
          disabled={!formValid}
          onClick={handleRegister}
          type="submit"
        >
          Зарегистрироваться
        </button>

        <button
          className="home-button"
          onClick={() => navigate("/auth")}
          type="button"
        >
          Вход
        </button>
      </div>

      {popupMessage && <Popup message={popupMessage} onClose={closePopup} duration={3000} />}
    </div>
  );
};

export default Register;

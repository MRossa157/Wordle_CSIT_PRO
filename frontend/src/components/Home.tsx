import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";
import Logo from "../Logo.png";
import Popup from "./Popup";
import Leaderboard from "./Leaderboard"; 

interface UserInfo {
  username: string;
}

const Home: React.FC = () => {
  const navigate = useNavigate();
  const [userInfo, setUserInfo] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refreshTokens = async (): Promise<boolean> => {
    try {
      const response = await fetch("http://localhost:5002/auth/tokens", {
        method: "POST",
        credentials: "include",
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log("Токены успешно обновлены:", data);
        return true;
      } else {
        console.error("Ошибка при обновлении токенов");
        return false;
      }
    } catch (error) {
      console.error("Ошибка соединения при обновлении токенов:", error);
      return false;
    }
  };
  

  useEffect(() => {
    refreshTokens();
    const storedUserData = sessionStorage.getItem("userInfo");

    if (storedUserData) {
      const { username } = JSON.parse(storedUserData) as UserInfo;
      setUserInfo(username);
    } else {
      const fetchData = async () => {
        try {
          const response = await fetch("http://localhost:5002/account/user_information", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
          });

          if (response.ok) {
            const data: UserInfo = await response.json();
            setUserInfo(data.username);
            sessionStorage.setItem("userInfo", JSON.stringify(data));
          }
        } catch (error) {
          console.error("Ошибка при отправке запроса:", error);
        }
      };

      fetchData();
    }
  }, []);

  const handleLoginClickApp = () => {
    navigate("/auth");
  };

  const handleLogout = async () => {
    try {
      const response = await fetch("http://localhost:5002/auth/logout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });

      if (response.ok) {
        sessionStorage.removeItem("userInfo");
        setUserInfo(null);
        navigate("/");
      } else {
        console.error("Ошибка при выходе из аккаунта");
      }
    } catch (error) {
      console.error("Ошибка при отправке запроса на выход:", error);
    }
  };

  const handlePlayClick = async () => {

    try {
      const response = await fetch("http://localhost:5002/wordle/create_game_session", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });

      if (response.ok) {
        const data: { session_id: string } = await response.json();
        const { session_id } = data;

        localStorage.setItem("sessionId", session_id);
        navigate("/game");
      } else {
        setError("Не удалось создать игровую сессию");
      }
    } catch (error: unknown) {
      setError("Ошибка при отправке запроса: " + (error instanceof Error ? error.message : "Неизвестная ошибка"));
    }
  };

  return (
    <div className="box">
      <img src={Logo} alt="Logo" className="logo" />
      <div className="info">
        <p className="title">Wordle</p>
        <p className="subtitle">Угадай 5-буквенное слово с 6 попыток.</p>
        <div className="mainButtons">
          {!userInfo && (
            <button onClick={handleLoginClickApp} className="home-button">
              Войти
            </button>
          )}
          <button onClick={handlePlayClick} className="home-button">
            Играть
          </button>
        </div>
      </div>

      {userInfo && (
        <div className="username-container">
          <span className="username">{userInfo}</span>
          <button className="logout-button" onClick={handleLogout}>
            Выйти
          </button>
        </div>
      )}

      {error && <Popup message={error} onClose={() => setError(null)} duration={3000} />}

      <div>
        <Leaderboard />
      </div>
    </div>
  );
};

export default Home;

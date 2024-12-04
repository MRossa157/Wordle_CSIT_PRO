import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { GameContext } from "./Game";
import "../App.css";

interface GameContextType {
  currAttempt: { attempt: number; letter: number };
  gameOver: { gameOver: boolean; guessedWord: boolean };
}

const GameOver: React.FC = () => {
  const gameContext = useContext(GameContext);
  const navigate = useNavigate();

  if (!gameContext) {
    return null; 
  }

  const { currAttempt, gameOver, correctWord } = gameContext;

  const handleGoHome = () => {
    navigate("/"); 
  };

  return (
    <div className="gameover">
      <h3>{gameOver.guessedWord ? "Молодец" : "Не молодец"}</h3>
      {gameOver.guessedWord && (
        <h3>Ты угадал за {currAttempt.attempt} попыток</h3>
      )}
      {!gameOver.guessedWord && (
        <h3>Правильное слово: {correctWord}</h3>
      )}
      <button onClick={handleGoHome} className="home-button">
        На главный экран
      </button>
    </div>
  );
};


export default GameOver;

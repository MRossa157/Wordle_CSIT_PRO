import "../App.css";
import Board, { boardDefault } from "./Board";
import Keyboard from "./Keyboard";
import React, { useState, createContext, useEffect } from "react";
import GameOver from "./GameOver";
import  Popup from "./Popup"

interface CurrAttempt {
  attempt: number;
  letter: number;
}

interface GameOverState {
  gameOver: boolean;
  guessedWord: boolean;
}

interface CheckResults {
  [key: number]: string[];
}

interface KeyValColor {
  [key: string]: string;
}

interface GameContextProps {
  board: string[][];
  setBoard: React.Dispatch<React.SetStateAction<string[][]>>;
  currAttempt: CurrAttempt;
  setCurrAttempt: React.Dispatch<React.SetStateAction<CurrAttempt>>;
  setCorrectWord: React.Dispatch<React.SetStateAction<string>>;
  correctWord: string;
  onSelectLetter: (key: string) => void;
  onDelete: () => void;
  onEnter: () => void;
  gameOver: GameOverState;
  checkResults: CheckResults;
  keyValColor: KeyValColor;
}

export const GameContext = createContext<GameContextProps | undefined>(undefined);

function Game() {
  const [board, setBoard] = useState<string[][]>(boardDefault);
  const [currAttempt, setCurrAttempt] = useState<CurrAttempt>({ attempt: 0, letter: 0 });
  const [correctWord, setCorrectWord] = useState<string>("");
  const [gameOver, setGameOver] = useState<GameOverState>({
    gameOver: false,
    guessedWord: false,
  });
  const [popupMessage, setPopupMessage] = useState<string | null>(null);
  const [checkResults, setCheckResults] = useState<CheckResults>({});
  const [keyValColor, setKeyValColor] = useState<KeyValColor>({});

  const showPopup = (message: string) => {
    setPopupMessage(message);
    setTimeout(() => setPopupMessage(null), 3000);
  };

  const closePopup = () => {
    setPopupMessage(null);
  };

  const resetGame = () => {
    const newBoard = board.map((row) => row.map(() => ""));
    setBoard(newBoard);
    setCurrAttempt({ attempt: 0, letter: 0 });
    setGameOver({ gameOver: false, guessedWord: false });
    setCheckResults({});
    setKeyValColor({});
  };
  
  useEffect(() => {
    resetGame();
  }, []);
  

  const onEnter = async () => {
    if (currAttempt.letter !== 5) return;
  
    let currWord = "";
    for (let i = 0; i < 5; i++) {
      currWord += board[currAttempt.attempt][i];
    }
  
    const session_id = localStorage.getItem("sessionId");
  
    try {
      const response = await fetch("http://localhost:5002/wordle/check_word", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: session_id,
          word: currWord.toLowerCase(),
        }),
        credentials: "include",
      });

      console.log(session_id)
  
      if (response.ok) {
        const data = await response.json();
        const { game_status, check_result, attempt_number, word_to_guess } = data as {
          game_status: string;
          check_result: Record<string, string>;
          attempt_number: number;
          word_to_guess: string;
        };
      
        if (game_status === "LOSS") {
          setCorrectWord(word_to_guess.toUpperCase());
        }
  
        const upperCaseCheckResult: Record<string, string> = Object.fromEntries(
          Object.entries(check_result).map(([key, value]) => [key.toUpperCase(), value])
        );
  
        setKeyValColor((prevKeyValColor) => ({
          ...prevKeyValColor,
          ...upperCaseCheckResult,
        }));
  
        const attemptResult = Array.from(currWord).map((letter) => {
          const upperLetter = letter.toUpperCase();
          return upperCaseCheckResult[upperLetter];
        });
  
        setCheckResults((prev) => ({
          ...prev,
          [currAttempt.attempt]: attemptResult,
        }));
  
        setCurrAttempt({ attempt: attempt_number, letter: 0 });
  
        if (game_status === "WIN") {
          setGameOver({ gameOver: true, guessedWord: true });
        } else if (attempt_number >= 6) {
          setGameOver({ gameOver: true, guessedWord: false });
        }
      }
      else{
        showPopup("Не в списке слов");
      }
    } catch (error) {
      console.error("Ошибка при соединении с сервером:", error);
    }
  };
  
  const onDelete = () => {
    if (currAttempt.letter === 0) return;
    const newBoard = [...board];
    newBoard[currAttempt.attempt][currAttempt.letter - 1] = "";
    setBoard(newBoard);
    setCurrAttempt({ ...currAttempt, letter: currAttempt.letter - 1 });
  };

  const onSelectLetter = (key: string) => {
    if (currAttempt.letter > 4) return;
    const newBoard = [...board];
    newBoard[currAttempt.attempt][currAttempt.letter] = key;
    setBoard(newBoard);
    setCurrAttempt({
      attempt: currAttempt.attempt,
      letter: currAttempt.letter + 1,
    });
  };

  return (
    <div className="Game">
      <GameContext.Provider
        value={{
          board,
          setBoard,
          currAttempt,
          setCurrAttempt,
          correctWord,
          onSelectLetter,
          setCorrectWord,
          onDelete,
          onEnter,
          gameOver,
          checkResults,
          keyValColor,
        }}
      >
        <div className="game">
          <Board />
          {gameOver.gameOver ? <GameOver /> : <Keyboard />}
          {popupMessage && <Popup message={popupMessage} onClose={closePopup} duration={3000} />}
        </div>
      </GameContext.Provider>
    </div>
  );
}

export default Game;

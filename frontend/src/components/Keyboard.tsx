import React, { useCallback, useEffect, useContext, useMemo } from "react";
import Key from "./Key";
import { GameContext } from "./Game";

const Keyboard: React.FC = () => {
  const keys1 = useMemo(() => ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"], []);
  const keys2 = useMemo(() => ["A", "S", "D", "F", "G", "H", "J", "K", "L"], []);
  const keys3 = useMemo(() => ["Z", "X", "C", "V", "B", "N", "M"], []);

  const gameContext = useContext(GameContext);

  const handleKeyboard = useCallback(
    (event: KeyboardEvent) => {
      if (!gameContext || gameContext.gameOver.gameOver) return;

      const { onEnter, onDelete, onSelectLetter } = gameContext;

      if (event.key === "Enter") {
        onEnter();
      } else if (event.key === "Backspace") {
        onDelete();
      } else {
        [...keys1, ...keys2, ...keys3].forEach((key) => {
          if (event.key.toLowerCase() === key.toLowerCase()) {
            onSelectLetter(key);
          }
        });
      }
    },
    [gameContext, keys1, keys2, keys3]
  );

  useEffect(() => {
    document.addEventListener("keydown", handleKeyboard);

    return () => {
      document.removeEventListener("keydown", handleKeyboard);
    };
  }, [handleKeyboard]);

  if (!gameContext) {
    return null;
  }

  const { currAttempt, gameOver } = gameContext;

  return (
    <div className="keyboard">
      <div className="line1">
        {keys1.map((key) => (
          <Key key={key} keyVal={key} />
        ))}
      </div>
      <div className="line2">
        {keys2.map((key) => (
          <Key key={key} keyVal={key} />
        ))}
      </div>
      <div className="line3">
        <Key key="ENTER" keyVal="ENTER" bigKey />
        {keys3.map((key) => (
          <Key key={key} keyVal={key} />
        ))}
        <Key key="DELETE" keyVal="DELETE" bigKey />
      </div>
    </div>
  );
};

export default Keyboard;

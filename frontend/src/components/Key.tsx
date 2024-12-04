import React, { useContext } from "react";
import { motion } from "framer-motion";
import { GameContext } from "./Game";

interface KeyProps {
  keyVal: string;
  bigKey?: boolean;
}

interface GameContextType {
  gameOver: { gameOver: boolean };
  onSelectLetter: (key: string) => void;
  onDelete: () => void;
  onEnter: () => Promise<void>;
  keyValColor: { [key: string]: string };
}

const Key: React.FC<KeyProps> = ({ keyVal, bigKey }) => {
  const gameContext = useContext(GameContext);

  if (!gameContext) {
    return null;
  }

  const { gameOver, onSelectLetter, onDelete, onEnter, keyValColor = {} } = gameContext;

  const selectLetter = () => {
    if (gameOver.gameOver) return;

    if (keyVal === "ENTER") {
      onEnter();
    } else if (keyVal === "DELETE") {
      onDelete();
    } else {
      onSelectLetter(keyVal);
    }
  };

  const keyColor = keyValColor[keyVal] || "";
  const keyState =
    keyColor === "GREEN"
      ? "correct"
      : keyColor === "YELLOW"
      ? "almost"
      : keyColor === "BLACK"
      ? "error"
      : "";

  return (
    <motion.div
      className={`key ${keyState} ${bigKey ? "big" : ""}`}
      onClick={selectLetter}
      key={keyState} 
      initial={{ y: 0 }}
      animate={{ y: [0, -10, 0] }} 
      transition={{
        type: "spring",
        stiffness: 500,
        damping: 10,
        duration: 0.3,
      }}
      whileHover={{
        scale: 1.1,
        transition: { type: "spring", stiffness: 300 },
      }}
      whileTap={{
        scale: 0.9,
        transition: { type: "spring", stiffness: 300 },
      }}
    >
      {keyVal}
    </motion.div>
  );
};

export default Key;
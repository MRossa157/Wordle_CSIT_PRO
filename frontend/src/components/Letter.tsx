import React, { useContext } from "react";
import { GameContext } from "./Game";
import { motion } from "framer-motion";


interface GameContextType {
  board: string[][];
  checkResults: Record<number, Record<number, "GREEN" | "YELLOW" | "BLACK" | undefined>>;
}


interface LetterProps {
  letterPos: number; 
  attemptVal: number; 
}

const Letter: React.FC<LetterProps> = ({ letterPos, attemptVal }) => {
  const gameContext = useContext(GameContext);

  if (!gameContext) {
    return null; 
  }

  const { board, checkResults } = gameContext;
  const letter = board[attemptVal]?.[letterPos] || "";
  const checkResult = checkResults[attemptVal] || {};
  const letterColor = checkResult[letterPos];

  const letterState =
    letterColor === "GREEN"
      ? "correct"
      : letterColor === "YELLOW"
      ? "almost"
      : letterColor === "BLACK"
      ? "error"
      : "";

  return (
    <motion.div
      className={`letter ${letterState}`}
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ type: "spring", stiffness: 300 }}
      whileHover={{ scale: 1.1 }} 
    >
      {letter}
    </motion.div>
  );
};

export default Letter;

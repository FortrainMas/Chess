import React, { useState } from "react";
import { useSelector } from "react-redux";
import blackRook from "../assets/pieces/black_rook.png";
import blackKnight from "../assets/pieces/black_knight.png";
import blackBishop from "../assets/pieces/black_bishop.png";
import blackQueen from "../assets/pieces/black_queen.png";
import blackKing from "../assets/pieces/black_king.png";
import blackPawn from "../assets/pieces/black_pawn.png";
import whiteRook from "../assets/pieces/white_rook.png";
import whiteKnight from "../assets/pieces/white_knight.png";
import whiteBishop from "../assets/pieces/white_bishop.png";
import whiteQueen from "../assets/pieces/white_queen.png";
import whiteKing from "../assets/pieces/white_king.png";
import whitePawn from "../assets/pieces/white_pawn.png";

function GameField({ makeMove }) {
  const field = useSelector((state) => state.field);
  const [selectedPiece, setSelectedPiece] = useState(null);

  const pieceImages = {
    r: blackRook,
    n: blackKnight,
    b: blackBishop,
    q: blackQueen,
    k: blackKing,
    p: blackPawn,
    R: whiteRook,
    N: whiteKnight,
    B: whiteBishop,
    Q: whiteQueen,
    K: whiteKing,
    P: whitePawn,
  };

  const handleCellClick = (row, col) => {
    if (selectedPiece) {
      if (field[row][col] === selectedPiece.piece) {
        setSelectedPiece(null);
        return;
      }

      makeMove([[selectedPiece.row, selectedPiece.col], [row, col]]);
      setSelectedPiece(null);
    } else if (field[row][col]) {
      setSelectedPiece({ piece: field[row][col], row, col });
    }
  };

  return (
    <div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(8, 1fr)", gap: 0 }}>
        {field.map((row, rowIndex) =>
          row.map((cell, colIndex) => {
            const isSelected = selectedPiece && selectedPiece.row === rowIndex && selectedPiece.col === colIndex;

            return (
              <div
                key={`${rowIndex}-${colIndex}`}
                onClick={() => handleCellClick(rowIndex, colIndex)}
                style={{
                  width: "50px",
                  height: "50px",
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  backgroundColor: isSelected
                    ? "#646cff"
                    : (rowIndex + colIndex) % 2 === 0
                    ? "#f0d9b5"
                    : "#b58863",
                  border: "1px solid #000",
                }}
              >
                {cell && (
                  <img
                    src={pieceImages[cell]}
                    alt={cell}
                    style={{ width: "40px", height: "40px" }}
                  />
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default GameField;

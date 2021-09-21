from chessboard import ChessBoard
from chesspiece import ChessPiece
from uuid import UUID
from fastapi import FastAPI
from fastapi.testclient import TestClient

board = ChessBoard()

app = FastAPI()


@app.post("/")
def post_piece(pieceType: str, pieceColor: str):
    piece = ChessPiece(pieceType, pieceColor)

    if type(piece) is dict:
        board.addPieceToList(piece)
        return {"Id": piece["id"]}

    return {"error": piece}


@app.put("/")
def put_board(id: UUID, position: str):
    result = board.addPieceToBoard(id, position)

    if type(result) is str:
        if result == "PIECE ADDED":
            return {"success": result}
        return {"error": result}

    return {"possibleLocations": result}

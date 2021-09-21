from chessboard import ChessBoard
from chesspiece import ChessPiece
from uuid import UUID
from fastapi import FastAPI

board = ChessBoard()

app = FastAPI()


@app.post("{piece}")
def post_piece(pieceType: str, pieceColor: str):
    piece = ChessPiece(pieceType, pieceColor)

    if type(piece) is dict:
        board.addPieceToList(piece)
        return {"Id": piece["id"]}

    return {"error": piece}


@app.put("{id}&{position}")
def put_board(id: UUID, position: str):
    result = board.addPieceToBoard(id, position)

    if type(result) is str:
        return {"error": result}

    return {"possibleLocations": result}

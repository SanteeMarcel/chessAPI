from os import error
from .chessboard import ChessBoard
from .chesspiece import ChessPiece
from uuid import UUID
from fastapi import FastAPI
from pymongo import MongoClient

board = ChessBoard()

app = FastAPI()

connectedToDababase = False

try:
    f = open("../mongopassword.txt", "r")
    user, password = f.read().split("\n")
    client = MongoClient(
        f"mongodb+srv://{user}:{password}@cluster0.4uknf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.chess
    connectedToDababase = True
except error:
    print("COULD NOT CONNECT TO DATABASE")


@app.post("/")
def post_piece(pieceType: str, pieceColor: str):
    piece = ChessPiece(pieceType, pieceColor)

    if type(piece) is dict:
        board.addPieceToList(piece)
        db.actions.insert_one({"New Piece Created": str(
            piece["id"])}) if connectedToDababase else None
        return {"Id": piece["id"]}

    db.errors.insert_one({"error": piece}) if connectedToDababase else None
    return {"error": piece}


@app.put("/")
def put_board(id: UUID, position: str):
    result = board.addPieceToBoard(id, position)

    if type(result) is str:
        if result == "PIECE ADDED":
            db.actions.insert_one({"New Piece Added To Board": str(
                str(id) + "@" + position)}) if connectedToDababase else None
            return {"success": result}
        db.errors.insert_one(
            {"error": result}) if connectedToDababase else None
        return {"error": result}

    db.actions.insert_one({"Calculated Possible Locations": str(
        result)}) if connectedToDababase else None
    return {"possibleLocations": result}


@app.get("/")
def read_root():
    return {"hello": "world"}

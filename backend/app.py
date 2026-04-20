import os
from dotenv import load_dotenv
load_dotenv()
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from pymongo import AsyncMongoClient, ReturnDocument

# ------------------------------------------------------------------------ #
#                        Inicialització de l'aplicació                      #
# ------------------------------------------------------------------------ #

app = FastAPI(
    title="Gestor de Llibres API",
    summary="API REST amb FastAPI i MongoDB per gestionar una col·lecció de llibres.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------ #
#                     Configuració de la connexió amb MongoDB               #
# ------------------------------------------------------------------------ #

client = AsyncMongoClient(os.environ["MONGODB_URL"])
db = client.gestor_llibres
book_collection = db.get_collection("llibres")

# PyObjectId: convertim ObjectId de MongoDB a string serialitzable per JSON
PyObjectId = Annotated[str, BeforeValidator(str)]

# ------------------------------------------------------------------------ #
#                          Definició dels models                            #
# ------------------------------------------------------------------------ #

class BookModel(BaseModel):
    """Model que representa un llibre a la base de dades."""

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titol: str = Field(...)
    autor: str = Field(...)
    estat: str = Field(..., pattern="^(pendent|llegit)$")
    valoracio: Optional[int] = Field(default=None, ge=1, le=5)
    categoria: str = Field(...)
    persona: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "titol": "El nom de la rosa",
                "autor": "Umberto Eco",
                "estat": "pendent",
                "valoracio": 4,
                "categoria": "Novel·la",
                "persona": "Jordi",
            }
        },
    )


class UpdateBookModel(BaseModel):
    """Model per actualitzar un llibre (tots els camps són opcionals)."""

    titol: Optional[str] = None
    autor: Optional[str] = None
    estat: Optional[str] = Field(default=None, pattern="^(pendent|llegit)$")
    valoracio: Optional[int] = Field(default=None, ge=1, le=5)
    categoria: Optional[str] = None
    persona: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "estat": "llegit",
                "valoracio": 5,
            }
        },
    )


class BookCollection(BaseModel):
    """Contenidor per a una llista de llibres."""
    llibres: List[BookModel]


# ------------------------------------------------------------------------ #
#                              Endpoints CRUD                               #
# ------------------------------------------------------------------------ #

@app.post(
    "/llibres/",
    response_description="Afegir un nou llibre",
    response_model=BookModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(book: BookModel):
    """Crea un nou llibre i l'insereix a la base de dades."""
    new_book = await book_collection.insert_one(
        book.model_dump(by_alias=True, exclude=["id"])
    )
    created_book = await book_collection.find_one({"_id": new_book.inserted_id})
    return created_book


@app.get(
    "/llibres/",
    response_description="Llistar tots els llibres",
    response_model=BookCollection,
)
async def list_books(categoria: Optional[str] = None, estat: Optional[str] = None):
    """
    Retorna tots els llibres.
    Opcionalment es pot filtrar per `categoria` i/o `estat`.
    """
    query = {}
    if categoria:
        query["categoria"] = categoria
    if estat:
        query["estat"] = estat

    books = await book_collection.find(query).to_list(100)
    return BookCollection(llibres=books)


@app.get(
    "/llibres/{id}",
    response_description="Obtenir un llibre per ID",
    response_model=BookModel,
)
async def show_book(id: str):
    """Retorna un llibre concret pel seu ID."""
    if (book := await book_collection.find_one({"_id": ObjectId(id)})) is not None:
        return book
    raise HTTPException(status_code=404, detail=f"Llibre {id} no trobat")


@app.put(
    "/llibres/{id}",
    response_description="Actualitzar un llibre",
    response_model=BookModel,
)
async def update_book(id: str, book: UpdateBookModel):
    """Actualitza els camps indicats d'un llibre existent."""
    book_data = {k: v for k, v in book.model_dump().items() if v is not None}

    if not book_data:
        if (existing := await book_collection.find_one({"_id": ObjectId(id)})) is not None:
            return existing
        raise HTTPException(status_code=404, detail=f"Llibre {id} no trobat")

    updated = await book_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": book_data},
        return_document=ReturnDocument.AFTER,
    )
    if updated is not None:
        return updated
    raise HTTPException(status_code=404, detail=f"Llibre {id} no trobat")


@app.delete("/llibres/{id}", response_description="Eliminar un llibre")
async def delete_book(id: str):
    """Elimina un llibre de la base de dades."""
    result = await book_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Llibre {id} no trobat")

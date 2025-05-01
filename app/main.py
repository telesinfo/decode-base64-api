from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import Response
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import base64
import mimetypes
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN não encontrado no arquivo .env")

api_key_header = APIKeyHeader(name="Token")

app = FastAPI(
    title="Decode Base64 API",
    description="API para decodificar arquivos base64 em diferentes formatos",
    version="1.0.0"
)

class Base64Request(BaseModel):
    base64_string: str
    file_extension: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "base64_string": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
                "file_extension": "png"
            }
        }

async def verify_token(token: str = Depends(api_key_header)):
    if token != API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

@app.post("/decode", response_class=Response)
async def decode_base64(request: Base64Request, token: str = Depends(verify_token)):
    try:
        # Decodifica o string base64
        file_bytes = base64.b64decode(request.base64_string)
        
        # Define o tipo MIME com base na extensão
        content_type = mimetypes.guess_type(f"file.{request.file_extension}")[0]
        if not content_type:
            raise HTTPException(status_code=400, detail="Extensão de arquivo não suportada")
            
        # Retorna o arquivo decodificado com o tipo MIME apropriado
        return Response(
            content=file_bytes,
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename=decoded.{request.file_extension}"
            }
        )
        
    except base64.binascii.Error:
        raise HTTPException(status_code=400, detail="String base64 inválida")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 
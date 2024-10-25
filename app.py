from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from crewai import Crew, Process
from uuid import uuid4
from dotenv import load_dotenv
from enum import Enum
import time
import jwt
import os

app = FastAPI()

load_dotenv()

# Configuração JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_SECRET_KEY_ALGORITHM")

if SECRET_KEY is None or ALGORITHM is None:
    raise ValueError("Auth credentials not found")

class Input(BaseModel):
    prompt: str

@app.post("/generate/segment")
async def generate_segment(req: Input):
    try:
        from segment_ai.crew import SegmentAiCrew

        # print(f"Usuário autenticado: {current_user.get('email')}")
        start_time = time.time()

        run_id = uuid4()
        print(f"Run ID: {run_id}")

        crew_instance = SegmentAiCrew().crew()

        result = await crew_instance.kickoff_async(inputs={'prompt': req.prompt})

        end_time = time.time()
        execution_time = end_time - start_time

        return {
            "run_id": str(run_id),
            "segment": result.raw,
            "tempo_execucao": f"{execution_time}s",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    print(">>>>>>>>>>>> version V0.0.1")
    uvicorn.run(app, host="0.0.0.0", port=8085, reload=True)
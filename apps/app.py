from dotenv import load_dotenv
from elasticsearch_logstash_kibana.controllers.users import router
from fastapi import Depends, FastAPI

load_dotenv()

app = FastAPI()

PORT = 8000

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)

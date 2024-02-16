"""The Authentication Service Provider Implemented using GraphQL"""
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from graphql_server.index import schema

load_dotenv()

app = FastAPI()
graphql = GraphQL(schema)

@app.get('/')
async def main():
    """Default Get Request Handler"""
    return {"message":"This is the Authentication Service Provider."}

app.add_route('/graphql', graphql)
# app.add_api_route('/auth', authController)

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 5000, reload=True)

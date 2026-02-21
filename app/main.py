from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    username: str


users = {}

next_users_id = len(users)


@app.get("/users")
async def read_users(username: str = None, limit: int = 10):
    filtered_users = users

    if username:
        filtered_users = {
            key: user
            for key, user in filtered_users.items()
            if username.lower() in user["username"].lower()
        }

    return dict(list(filtered_users.items())[:limit])


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id in users:
        return {"id": user_id, **users[user_id]}
    return {"error": "User not found"}


@app.post("/add_user", response_model=User)
async def add_user(user: User):
    global next_users_id
    users[next_users_id] = {"username": user.username}
    next_users_id += 1
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id in users:
        del users[user_id]
    return {"message": f"User {user_id} deleted succesfully!"}

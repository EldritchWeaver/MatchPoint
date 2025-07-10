
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.1.108", port=8000, reload=True)


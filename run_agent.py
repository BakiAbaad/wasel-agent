from uvicorn import run

if __name__ == "__main__":
    # run the FastAPI app in simple mode for Windows
    run("app.main:app", host="127.0.0.1", port=8000)

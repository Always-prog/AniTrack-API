import uvicorn

if __name__ == '__main__':
    uvicorn.run("api:app",
                host="127.0.0.1",
                workers=4,
                port=8000,
                reload=True,
                ssl_keyfile="./localhost.decrypted.key",
                ssl_certfile="./localhost.crt",
                ssl_keyfile_password="1234",
                )
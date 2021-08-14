from fastapi import FastAPI

from server.app.Server import Server


server_class = Server()
server: FastAPI = server_class.get_instance()


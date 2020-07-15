from .Backend import Server

Server.app.serve(port=5000, use_reloader=False, use_meta=True, use_debugger=True)

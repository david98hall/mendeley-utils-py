import threading
import flask
import multiprocessing
import threading
import webbrowser

from mendeley import Mendeley
from mendeley.session import MendeleySession
from werkzeug.serving import make_server

class FlaskServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        # self.ctx = app.app_context()
        # self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

class MendeleyHelper:

    def __init__(self, client_id: str, client_secret: str) -> None:
        
        oath_route = "/oauth"
        self.__server_uri = "http://localhost:5000"
        redirect_uri = f'{self.__server_uri}{oath_route}'
        self.__mendeley = Mendeley(client_id, client_secret, redirect_uri)
        self.__mendeley_session_queue = multiprocessing.Queue()
        self.__session_token = None
        self.__mendeley_state = None

        self.__app = flask.Flask("__main__")
        self.__app.debug = False
        self.__app.secret_key = client_secret

        self.__app.route("/")(self.__login)
        self.__app.route(oath_route)(self.__auth_return)

    def get_session(self, use_existing_token=True):
        if not use_existing_token or self.__session_token is None:
            self.__session_token = self.__get_session_token()
        return MendeleySession(self.__mendeley, self.__session_token)

    def __get_session_token(self):
        thread = FlaskServerThread(app=self.__app)
        thread.start()
        webbrowser.open(self.__server_uri)
        session_token = self.__mendeley_session_queue.get(block=True)
        thread.shutdown()

        return session_token

    def __login(self):
        auth = self.__mendeley.start_authorization_code_flow()
        self.__mendeley_state = auth.state
        
        login_url = auth.get_login_url()
        return flask.redirect(login_url)

    def __auth_return(self):
        auth = self.__mendeley.start_authorization_code_flow(state=self.__mendeley_state)
        mendeley_session = auth.authenticate(flask.request.url)
        self.__mendeley_session_queue.put(mendeley_session.token)
        return flask.render_template("successful.html")

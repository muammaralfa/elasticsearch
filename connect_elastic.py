from elasticsearch import Elasticsearch


class Connection:
    """
        this es connection initialized is using an elastich version 7.13
    """
    def __init__(self):
        self.host = "host"
        self.port = "port"
        self.user = "user"
        self.password = "password"
        self.es = Elasticsearch(
            host=self.host,
            port=self.port,
            sceheme='http',
            http_auth=(self.user, self.password)
        )

    def connect(self):
        return self.es

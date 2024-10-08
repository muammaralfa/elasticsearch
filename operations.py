from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from connection import Connection


class Operations:
    def __init__(self):
        self.conn = Connection().connect()

    def _search(self):
        """
        get data from elastic
        :return:
        """

        datas = self.conn.search(
            index='index',
            size=100, # default size. max persearch is 1000 greater u have to use scroll or pit
            query={
                "match": {
                    "name": "alfa"
                }
            },
            timeout=3600
        )
        if datas['hits']['hits']:
            for data in datas['hits']['hits']:
                source = data['_source']
                id = data['_id']

    def _scroll(self):
        """
        scroll biasanya dipake kalo ngambil data banyak. karena limit dari es cuman 1000 docs,
        maka pake scroll ambil per1000 setelah beres ambil lagi dengan token scroll (lanjut dari last doc)

        scroll tidak akan berhentu hingga document paling terakahir (tergantung query)
        :return:
        """

        datas = self.conn.search(
            index='index_name',
            query={
                "match_all": {}
            },
            scroll='5m'
        )
        scroll_id = datas['_scroll_id']
        scroll_size = len(datas['hits']['hits'])
        while scroll_size > 0:
            for data in datas['hits']['hits']:
                pass
                # do something

            datas = self.conn.scroll(scroll_id=scroll_id, scroll='10m')
            scroll_id = datas['_scroll_id']
            scroll_size = len(datas['hits']['hits'])

    def _fetch_data(self, docs: list):
        """
        method pendukung untuk melakukan streaming bulk ke es,
        fungsi nya untuk mengeluarkan yield actions di dalam list document

        :param docs:
        :return:
        """
        for doc in docs:
            yield doc

    def _bulk(self, es, docs: list):
        """
        bulk biasanya digunakan untuk ingest/update/delete data secara bersamaan
        sistemnya memasukan list actions kedalam streaming bulk

        :param es:
        :param docs:
        :return:
        """
        for success, info in streaming_bulk(
                client=es,
                actions=self._fetch_data(docs),
                chunk_size=100,
                raise_on_exception=False,
                raise_on_error=False
        ):
            if not success:
                pass

            print(success, info)
            docs.clear()




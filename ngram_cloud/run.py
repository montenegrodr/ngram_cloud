import json
import cherrypy

import ngram_cloud.orm as orm


class App(object):
    @cherrypy.expose
    def vocab(self):
        with orm.VocabController() as controller:
            vocab = [{v.word: v.occurrences} for v in controller.list()]
            cherrypy.serving.response.headers['Content-type'] = 'application/json; chartset=utf-8'
            return json.dumps(vocab).encode('utf-8')


cherrypy.quickstart(App())

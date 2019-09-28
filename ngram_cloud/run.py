import json
import cherrypy

import ngram_cloud.controllers as controllers


class App(object):
    @cherrypy.expose
    def vocab(self):
        with controllers.VocabController() as vocab_controller:
            vocab = [{v.word: v.occurrences} for v in vocab_controller.list()]
            cherrypy.serving.response.headers['Content-type'] = 'application/json; chartset=utf-8'
            return json.dumps(vocab).encode('utf-8')


cherrypy.quickstart(App())

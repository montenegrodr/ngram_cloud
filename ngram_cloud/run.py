import json

import cherrypy
import ngram_cloud.controllers as controllers


class App(object):
    @cherrypy.expose
    def vocab(self):
        with controllers.VocabController() as vocab_controller:
            vocab = [{v.word: v.occurrences} for v in vocab_controller.all()]
            cherrypy.serving.response.headers['Content-type'] = 'application/json; chartset=utf-8'
            return json.dumps(vocab).encode('utf-8')

    @cherrypy.expose
    def cloud(self, word, rate=None, solved=None):
        with controllers.CloudController() as cloud_controller:
            graph = cloud_controller.cloud(word, rate, solved)

        if False:
            cherrypy.serving.response.headers['Content-type'] = 'application/json; chartset=utf-8'
            return json.dumps(graph.to_json()).encode('utf-8')
        else:
            retobj = cherrypy.lib.static.serve_fileobj(graph.to_img_bytes(), content_type='png', name='cloud.png')
            return retobj


cherrypy.quickstart(App())


import sys
import json
import logging
import cherrypy
import ngram_cloud.controllers as controllers


class App(object):
    def __init__(self, logger):
        self.logger = logger

    @cherrypy.expose
    def vocab(self):
        with controllers.VocabController() as vocab_controller:
            vocab = [{v.word: v.occurrences} for v in vocab_controller.all()]
            cherrypy.serving.response.headers['Content-type'] = 'application/json; chartset=utf-8'
            return json.dumps(vocab).encode('utf-8')

    @cherrypy.expose
    def cloud(self, word, rate=None, solved=None, output='png'):
        try:
            with controllers.CloudController() as cloud_controller:
                graph = cloud_controller.cloud(word, rate, solved)
            if output == 'json' or 'application/json' in cherrypy.serving.request.headers.get('Accept'):
                cherrypy.serving.response.headers['Content-type'] = 'application/json; chartset=utf-8'
                return json.dumps(graph.to_json()).encode('utf-8')
            else:
                return cherrypy.lib.static.serve_fileobj(
                    graph.to_img_bytes(),
                    content_type='png',
                    name='cloud.png'
                )

        except controllers.NgramCloudException as exp:
            self.logger.info(exp)
            cherrypy.serving.response.status = 400
            return json.dumps({
                'error': str(exp)
            })
        except Exception as exp:
            # Not good to catch all exceptions, but this
            # is the last customer facing layer
            self.logger.info(exp)
            cherrypy.serving.response.status = 500
            return json.dumps({
                'error': 'Unknown error'
            })


def main(logger):
    logger.info('Starting application..')
    cherrypy.quickstart(App(logger))


def setup_logger():
    logger = logging.getLogger('ngram_cloud')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


if __name__ == '__main__':
    main(setup_logger())

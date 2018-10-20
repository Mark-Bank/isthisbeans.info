import os
import logging
import logging.handlers

from wsgiref.simple_server import make_server


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler 
LOG_FILE = '/opt/python/log/sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)

api_key = os.environ['visual_recognition_api_key']
api_endpoint = os.environ['visual_recognition_base_endpoint']



#curl -X POST -u "apikey:${api_key}" \
#--form "images_file=@${images_dir}/beans.jpg" \
#"https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2018-03-19"

def application(environ, start_response):
    logger.info("WOO! api_endpoint: %s" % api_endpoint)
    path    = environ['PATH_INFO']
    method  = environ['REQUEST_METHOD']
    if method == 'POST':
        try:
            if path == '/':
                request_body_size = int(environ['CONTENT_LENGTH'])
                request_body = environ['wsgi.input'].read(request_body_size).decode()
                logger.info("Received message: %s" % request_body)
                logger.info("... you some kind of POSTal service? >:)")
            elif path == '/scheduled':
                logger.info("Received task %s scheduled at %s", environ['HTTP_X_AWS_SQSD_TASKNAME'], environ['HTTP_X_AWS_SQSD_SCHEDULED_AT'])
        except (TypeError, ValueError):
            logger.warning('Error retrieving request body for async work.')
        response = ''
    else:
        logger.info("... you're a real go-getter, eh? >:)")
        # TODO use a real framework at some point, eh
        with open('static/index.html', 'r') as my_index:
            response = my_index.read()
    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)
    return [response]


if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()

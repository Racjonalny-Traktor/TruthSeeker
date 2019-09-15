from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_cors import CORS
import datetime


from .utils import get_opposite_articles

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
    parser.add_argument('publication_date', type=str)
parser.add_argument('domain', type=str)
args = parser.parse_args()

def get_time_delta(datestring):
    datetime_object = datetime.strptime(datetime_str, '%m/%d/%y

class RateArticle(Resource):
    def post(self):
        args = parser.parse_args()
        errors = []
        opposition = get_opposite_articles(args['title'], args['domain'])
        token = 'gf3f4v36f6v3fv6i7346f'
        return {
            'errors': errors,
            'opposition_articles': opposition,
            'feedback_token': token
        }

class ProvideFeedback(Resource):
    def get(self, token, rate):
        errors = []
        opposition = []
        token = ''
        return {
            'errors': errors,
            'opposition_articles': opposition,
            'feedback_token': token
        }

api.add_resource(RateArticle, '/article')
api.add_resource(RateArticle, '/feedback/<token>/<rate>/')

if __name__ == '__main__':
    app.run(debug=True)

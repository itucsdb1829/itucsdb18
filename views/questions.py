from flask_restful import reqparse, Resource
from models.users import Users
from models.questions import Questions
from models.feedbacks import FeedBacks
from views.auth import auth


class QuestionsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('question_image', type=str)
        self.parser.add_argument('answer_image', type=str)
        self.parser.add_argument('choice', type=str)
        self.parser.add_argument('course', type=str)
        self.parser.add_argument('subject', type=str)
        self.parser.add_argument('comment', type=str)
        self.parser.add_argument('teacher', type=dict)

    def get(self, id):
        q = Questions.get(id=id)
        if q:
            if q.teacher:
                q.teacher = q.teacher.__dict__
                q.teacher['full_name'] = '{} {}'.format(q.teacher['name'], q.teacher['surname'])
            return q.__dict__
        return {}, 404

    def put(self, id):
        args = self.parser.parse_args()
        q = Questions.get(id=id)
        if q and args:
            if args.get('teacher'):
                t = Users.get(email=args.get('teacher', {}).get('email'))
                args['teacher'] = t.id
                if not t:
                    args['teacher'] = None
            q.update(**args)
            return q.__dict__
        return {}, 404

    def delete(self, id):
        q = Questions.get(id=id)
        if q:
            if q.teacher:
                q.teacher = q.teacher.__dict__
            r = q.__dict__
            q.delete()
            return r, 200


class QuestionListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('question_image', type=str)
        self.parser.add_argument('answer_image', type=str)
        self.parser.add_argument('choice', type=str)
        self.parser.add_argument('course', type=str)
        self.parser.add_argument('subject', type=str)
        self.parser.add_argument('comment', type=str)
        self.parser.add_argument('teacher', type=dict)

    def get(self):
        qs = Questions.filter()
        if qs:
            r = []
            for q in qs:
                feedbacks = q.get_feedbacks()
                if q.teacher:
                    q.teacher = q.teacher.__dict__
                    q.teacher['full_name'] = '{} {}'.format(q.teacher['name'], q.teacher['surname'])
                q = q.__dict__
                q['feedbacks'] = feedbacks
                r.append(q)
            return r, 200
        return {}, 404

    def post(self):
        args = self.parser.parse_args()
        print(args)
        if args:
            if args.get('teacher'):
                t = Users.get(email=args.get('teacher', {}).get('email'))
                args['teacher'] = t
                if not t:
                    args['teacher'] = None
            q = Questions.create(**args)
            if q.teacher:
                q.teacher = q.teacher.__dict__
            return q.__dict__
        return {}, 404

from flask_restful import reqparse, Resource
from models.users import Users
from models.questions import Questions
from models.feedbacks import FeedBacks
from views.auth import auth


class FeedbacksAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('question', type=dict)
        self.parser.add_argument('comment', type=str)
        self.parser.add_argument('quality_rate', type=int)
        self.parser.add_argument('difficulty_rate', type=int)
        self.parser.add_argument('is_proper', type=bool)
        self.parser.add_argument('reviewer', type=dict)

    def get(self, id):
        fb = FeedBacks.get(id=id)
        if fb:
            if fb.reviewer:
                fb.reviewer = fb.reviewer.__dict__
            if fb.created_at:
                fb.created_at = fb.created_at.isoformat()
            if fb.question:
                if fb.question.teacher:
                    fb.question.teacher = fb.question.teacher.__dict__
                fb.question = fb.question.__dict__
            return fb.__dict__
        return {}, 404

    def put(self, id):
        args = self.parser.parse_args()
        fb = FeedBacks.get(id=id)
        if fb and args:
            if args.get('reviewer'):
                t = Users.get(email=args.get('reviewer', {}).get('email'))
                args['reviewer'] = None
                if t:
                    args['reviewer'] = t.id
            if args.get('question'):
                q = Questions.get(id=args.get('question', {}).get('id'))
                args['question'] = None
                if q:
                    args['question'] = q.id
            fb.update(**args)
            if fb.reviewer:
                fb.reviewer = fb.reviewer.__dict__
            if fb.created_at:
                fb.created_at = fb.created_at.isoformat()
            if fb.question:
                if fb.question.teacher:
                    fb.question.teacher = fb.question.teacher.__dict__
                fb.question = fb.question.__dict__
            return fb.__dict__
        return {}, 404

    def delete(self, id):
        fb = FeedBacks.get(id=id)
        if fb:
            if fb.reviewer:
                fb.reviewer = fb.reviewer.__dict__
            if fb.created_at:
                fb.created_at = fb.created_at.isoformat()
            if fb.question:
                if fb.question.teacher:
                    fb.question.teacher = fb.question.teacher.__dict__
                fb.question = fb.question.__dict__
            r = fb.__dict__
            fb.delete()
            return r, 200


class FeedbackListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('question', type=dict)
        self.parser.add_argument('comment', type=str)
        self.parser.add_argument('quality_rate', type=int)
        self.parser.add_argument('difficulty_rate', type=int)
        self.parser.add_argument('is_proper', type=bool)
        self.parser.add_argument('reviewer', type=dict)

    def get(self):
        qs = FeedBacks.filter()
        if qs:
            r = []
            for fb in qs:
                if fb.reviewer:
                    fb.reviewer = fb.reviewer.__dict__
                if fb.created_at:
                    fb.created_at = fb.created_at.isoformat()
                if fb.question:
                    if fb.question.teacher:
                        fb.question.teacher = fb.question.teacher.__dict__
                    fb.question = fb.question.__dict__
                fb = fb.__dict__
                r.append(fb)
            return r, 200
        return {}, 404

    def post(self):
        args = self.parser.parse_args()
        print(args)
        if args:
            if args.get('reviewer'):
                t = Users.get(email=args.get('reviewer', {}).get('email'))
                args['reviewer'] = t
                if not t:
                    args['reviewer'] = None

            if args.get('question'):
                q = Questions.get(id=args.get('question', {}).get('id'))
                args['question'] = q
                if not q:
                    args['question'] = None

            fb = FeedBacks.create(**args)
            if fb.reviewer:
                fb.reviewer = fb.reviewer.__dict__
            if fb.created_at:
                fb.created_at = fb.created_at.isoformat()
            if fb.question:
                if fb.question.teacher:
                    fb.question.teacher = fb.question.teacher.__dict__
                fb.question = fb.question.__dict__
            return fb.__dict__
        return {}, 404

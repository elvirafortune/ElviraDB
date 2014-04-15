import datetime
from dbentities import user, forum, post, thread
import json
import re
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from database import DBconnect


@csrf_exempt
def choose_entity(request, entity, function):
    if request.method == 'POST':
        requestd = json.loads(request.body, encoding='utf-8')
    else:
        requestd = request.GET.dict()

    function = re.sub('/', '', function)

    if entity == "user":
        response_function = getattr(user, function)
    if entity == "forum":
        response_function = getattr(forum, function)
    if entity == "post":
        response_function = getattr(post, function)
    if entity == "thread":
        response_function = getattr(thread, function)
    try:
        result = response_function(**requestd)
        response_res = {
            'code': 0,
            'response': result
       }
    except Exception as e:
        response_res = {
            'code': 1,
            'response': str(e)
        }
    return HttpResponse(json.dumps(response_res, default=DateTime().default, ensure_ascii=False),
                        content_type='application/json')

class DateTime(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTime, self).default(obj)


@csrf_exempt
def deleteAll():
    db = DBconnect.connect()

    cur = db.cursor()
    cur.execute("set FOREIGN_KEY_CHECKS=0")
    cur.execute("TRUNCATE TABLE subscription")
    cur.execute("TRUNCATE TABLE followers")
    cur.execute("TRUNCATE TABLE post")
    cur.execute("TRUNCATE TABLE thread")
    cur.execute("TRUNCATE TABLE forum")
    cur.execute("TRUNCATE TABLE user")
    cur.execute("set FOREIGN_KEY_CHECKS=1")
    cur.close()

    db.close()

    pass
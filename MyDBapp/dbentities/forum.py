__author__ = 'Elvira'
from database import DBconnect
from MyDBapp.additions import SubscriptionsList, followers, StringToFile
import user, thread

def required(data, params):
    for param in params:
        if param not in data:
            raise Exception("Parameter '%s' is required" % param)

def create(**data):

    required(data, ['name', 'short_name', 'user'])

    db = DBconnect.connect()

    cur = db.cursor()
    cur.execute("""INSERT INTO forum
                   (name, short_name, user)
                   VALUES (%s, %s, %s)""",
                (data['name'], data['short_name'], data['user'],))
    db.commit()
    cur.close()

    cur = db.cursor()
    cur.execute("""SELECT *
                   FROM forum
                   WHERE short_name = %s""", (data['short_name'],))
    forum = cur.fetchone()
    cur.close()
    db.close()

    return forum


def details(db=0, close_db=True, **data):

    if 'forum' not in data:
        raise Exception("parameter 'forum' is required")

    if db == 0:
        db = DBconnect.connect()

    cur = db.cursor()

    cur.execute("""SELECT *
                   FROM forum
                   WHERE short_name = %s""", (data['forum'],))
    forum = cur.fetchone()
    cur.close()

    data['user'] = forum['user']

    if 'related' in data and len(data['related']) != 0 and data['related'] == 'user':
        cur = db.cursor()

        cur.execute("""SELECT id, email, isAnonymous, name
                       FROM user
                       WHERE email = %s""", (data['user'],))
        user_data = cur.fetchone()
        cur.close()

        user_data['isAnonymous'] = bool(user_data['isAnonymous'])
        user_data['subscriptions'] = SubscriptionsList(data['user'], db)
        user_data['followers'] = followers.Followerin(data, ['followers', 'short'], db)
        user_data['following'] = followers.Followerfrom(data, ['followees', 'short'], db)

        forum['user'] = user_data

    if close_db:
        db.close()

    return forum


def listPosts(**data):
    required(data, ['forum'])
    if 'order' not in data:
        data['order'] = 'desc'

    query = StringToFile.StringToFilefunc()
    params = ()
    query.append("""SELECT * FROM post
                    WHERE thread in (SELECT id FROM thread WHERE forum = %s)""")
    params += (data['forum'],)

    if 'since' in data:
        query.append(""" AND date >= %s""")
        params += (data['since'],)

    query.append(""" ORDER BY date %s""" % data['order'])

    if 'limit' in data:
        query.append(""" LIMIT %s""" % data['limit'])

    db = DBconnect.connect()
    cur = db.cursor()
    cur.execute(str(query), params)
    posts = cur.fetchall()
    cur.close()

    for post in posts:
        post['isApproved'] = bool(post['isApproved'])
        post['isDeleted'] = bool(post['isDeleted'])
        post['isEdited'] = bool(post['isEdited'])
        post['isHighlighted'] = bool(post['isHighlighted'])
        post['isSpam'] = bool(post['isSpam'])
        post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")

        if 'related' in data:
            if 'thread' in data['related']:
                thread_data = {'thread': post['thread']}
                thread_data = thread.details(db, False, **thread_data)
                post['thread'] = thread_data
            if 'user' in data['related']:
                user_data = {'user': post['user']}
                user_data = user.details(db, False, **user_data)
                post['user'] = user_data
            if 'forum' in data['related']:
                forum_data = {'forum': post['forum']}
                forum_data = details(db, False, **forum_data)
                post['forum'] = forum_data

    return posts
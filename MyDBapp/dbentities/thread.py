__author__ = 'Elvira'

from database import DBconnect
import forum
from MyDBapp.additions import StringToFile, SubscriptionsList, followers

def required(data, params):
    for param in params:
        if param not in data:
            raise Exception("Parameter '%s' is required" % param)

def create(**data):
    required(data, ['forum', 'title', 'isClosed', 'user', 'date', 'message', 'slug'])
    if 'isDeleted' not in data:
        data['isDeleted'] = False
    db = DBconnect.connect()
    cur = db.cursor()
    try:
        cur.execute("""INSERT INTO thread (forum, title, isClosed, isDeleted, user, date, message, slug, points)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0)""",
                    (data['forum'], data['title'], data['isClosed'], data['isDeleted'], data['user'], data['date'], data['message'], data['slug'],))
        db.commit()
    except Exception as e:
        cur.close()
        db.rollback()
        db.close()
        raise e
    cur.close()

    cur = db.cursor()
    cur.execute("""SELECT id, date, forum, isClosed, isDeleted, message, slug, title, user
                   FROM thread
                   WHERE slug = %s""", (data['slug'],))
    thread = cur.fetchone()
    cur.close()
    db.close()
    thread['date'] = thread['date'].strftime("%Y-%m-%d %H:%M:%S")
    thread['isDeleted'] = bool(thread['isDeleted'])
    thread['isClosed'] = bool(thread['isClosed'])
    return thread


def details(db=0, close_db=True, **data):
    required(data, ['thread'])
    if db == 0:
        db = DBconnect.connect()
    cur = db.cursor()
    cur.execute("""SELECT *
                   FROM thread
                   WHERE id = %s""", (data['thread'],))
    thread = cur.fetchone()
    cur.close()
    thread['date'] = thread['date'].strftime("%Y-%m-%d %H:%M:%S")
    thread['isDeleted'] = bool(thread['isDeleted'])
    thread['isClosed'] = bool(thread['isClosed'])
    if 'related' in data:
        if 'user' in data['related']:
            cur = db.cursor()
            cur.execute("""SELECT id, email, isAnonymous, name, username, about
                          FROM user
                          WHERE email = %s""", (thread['user'],))
            user_data = cur.fetchone()
            cur.close()
            user_data['isAnonymous'] = bool(user_data['isAnonymous'])
            user_data['subscriptions'] = SubscriptionsList.SubscriptionsListfunc(thread['user'], db)
            user_data['followers'] = followers.Followerin(thread, ['followers', 'short'], db)
            user_data['following'] = followers.Followerfrom(thread, ['followees', 'short'], db)
            thread['user'] = user_data
        if 'forum' in data['related']:
            forum_data = {'forum': thread['forum']}
            thread['forum'] = forum.details(db, False, **forum_data)
    if close_db:
        db.close()
    return thread


def close(**data):
    required(data, ['thread'])

    db = DBconnect.connect()
    cur = db.cursor()
    try:
        cur.execute("""UPDATE thread
                       SET isClosed = 1
                       WHERE id = %s""", (data['thread'],))
        db.commit()
    except Exception as e:
        cur.close()
        db.rollback()
        db.close()
        raise e
    cur.close()
    db.close()
    return {'thread': data['thread']}

def list(**data):
    if 'order' not in data:
        data['order'] = 'desc'
    if 'user' not in data and 'forum' not in data:
        raise Exception("Either user or forum is required")
    if 'user' in data and 'forum' in data:
        raise Exception("You can choose user or forum, but not both")
    db = DBconnect.connect()
    query = StringToFile.StringToFilefunc()
    params = ()
    if 'user' in data:
        query.append("""SELECT *
                       FROM thread
                       WHERE user = %s""")
        params += (data['user'],)
    elif 'forum' in data:
        query.append("""SELECT *
                       FROM thread
                       WHERE forum = %s""")
        params += (data['forum'],)

    if 'since' in data:
        query.append(""" AND date >= %s""")
        params += (data['since'],)

    if 'order' in data:
        query.append(""" ORDER BY date %s""" % data['order'])

    if 'limit' in data:
        query.append(""" LIMIT %s""" % data['limit'])

    cur = db.cursor()
    cur.execute(str(query), params)
    list = cur.fetchall()
    cur.close()
    for thread in list:
        thread['date'] = thread['date'].strftime("%Y-%m-%d %H:%M:%S")
    return list

def open(**data):
    required(data, ['thread'])

    db = DBconnect.connect()
    cur = db.cursor()
    try:
        cur.execute("""UPDATE thread
                       SET isClosed = 0
                       WHERE id = %s""", (data['thread'],))
        db.commit()
    except Exception as e:
        cur.close()
        db.rollback()
        db.close()
        raise e
    cur.close()
    db.close()
    return {'thread': data['thread']}


def remove(**data):
    required(data, ['thread'])
    db = DBconnect.connect()
    cur = db.cursor()
    try:
        cur.execute("""UPDATE thread
                       SET isDeleted = 1
                       WHERE id = %s""", (data['thread'],))
        db.commit()
    except Exception as e:
        cur.close()
        db.rollback()
        db.close()
        raise e
    cur.close()
    db.close()
    return {'thread': data['thread']}


def restore(**data):
    required(data, ['thread'])
    db = DBconnect.connect()
    cur = db.cursor()
    try:
        cur.execute("""UPDATE thread
                       SET isDeleted = 0
                       WHERE id = %s""", (data['thread'],))
        db.commit()
    except Exception as e:
        cur.close()
        db.rollback()
        db.close()
        raise e
    cur.close()
    db.close()
    return {'thread': data['thread']}

def update(**data):
    required(data, ['message', 'slug', 'thread'])
    db = DBconnect.connect()
    cur = db.cursor()
    try:
        cur.execute("""UPDATE thread
                       SET message = %s, slug = %s
                       WHERE id = %s""",
                    (data['message'], data['slug'], data['thread'],))
        db.commit()
    except Exception as e:
        cur.close()
        db.rollback()
        db.close()
        raise e
    cur.close()
    cur = db.cursor()
    cur.execute("""SELECT * FROM thread
                   WHERE id = %s""", (data['thread'],))
    thread = cur.fetchone()
    cur.close()
    db.close()
    thread['date'] = thread['date'].strftime("%Y-%m-%d %H:%M:%S")
    return thread



def vote(**data):

    required(data, ['thread', 'vote'])
    data['vote'] = int(data['vote'])
    if data['vote'] != -1 and data['vote'] != 1:
        raise Exception("Illegal vote.")
    db = DBconnect.connect()
    cur = db.cursor()
    try:
        if data['vote'] == -1:
            cur.execute("""UPDATE thread
                           SET dislikes = dislikes + 1,
                               points = points - 1
                           WHERE id = %s""", (data['thread'],))
        else:
            cur.execute("""UPDATE thread
                           SET likes = likes + 1,
                               points = points + 1
                           WHERE id = %s""", (data['thread'],))
        db.commit()
    except Exception as e:
        cur.close()
        db.rollback()
        db.close()
        raise e
    cur.close()
    thread = details(db, True, **data)
    return thread


def subscribe(**data):
    required(data, ['thread', 'user'])
    db = DBconnect.connect()
    cur = db.cursor()
    cur.execute("""SELECT * FROM subscription
                   WHERE user = %s AND thread = %s""", (data['user'], data['thread'],))
    exists = cur.fetchone()
    cur.close()
    cur = db.cursor()
    try:
        if not exists or len(exists) == 0:
            cur.execute("""INSERT INTO subscription
                           VALUES (%s, %s, 1)""", (data['user'], data['thread'],))
        else:
            cur.execute("""UPDATE subscription
                           SET isSubscribed = 1
                           WHERE user = %s AND thread = %s""", (data['user'], data['thread'],))
        db.commit()
    except Exception as e:
        db.rollback()
        cur.close()
        db.close()
        raise e
    cur.close()
    db.close()
    return {'thread': data['thread'], 'user': data['user']}


def unsubscribe(**data):
    required(data, ['thread', 'user'])

    db = DBconnect.connect()
    cur = db.cursor()
    cur.execute("""SELECT * FROM subscription
                   WHERE user = %s AND thread = %s""", (data['user'], data['thread'],))
    exists = cur.fetchone()
    cur.close()
    cur = db.cursor()
    try:
        if exists and len(exists) != 0:
            cur.execute("""UPDATE subscription
                           SET isSubscribed = 0
                           WHERE user = %s AND thread = %s""", (data['user'], data['thread'],))
            db.commit()
    except Exception as e:
        db.rollback()
        cur.close()
        db.close()
        raise e
    cur.close()
    db.close()
    return {'thread': data['thread'], 'user': data['user']}

def listPosts(**data):
    required(data, ['thread'])
    param = 'order'
    if param not in data:
        data[param] = 'desc'
    query = StringToFile.StringToFilefunc()
    params = ()
    query.append("""SELECT * FROM post
                    WHERE thread = %s""")
    params += (data['thread'],)

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
    db.close()
    for post in posts:
        post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")
        post['isApproved'] = bool(post['isApproved'])
        post['isDeleted'] = bool(post['isDeleted'])
        post['isEdited'] = bool(post['isEdited'])
        post['isHighlighted'] = bool(post['isHighlighted'])
        post['isSpam'] = bool(post['isSpam'])
    return posts






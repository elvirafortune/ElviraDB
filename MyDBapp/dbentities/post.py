__author__ = 'Elvira'

from database import DBconnect
from MyDBapp.additions import StringToFile
import user, forum, thread

def required(data, params):
    for param in params:
        if param not in data:
            raise Exception("Parameter '%s' is required" % param)

def create(**data):

    required(data, ['date', 'thread', 'message', 'user', 'forum'])
    if 'parent' not in data:
        data['parent'] = None

    if 'isApproved' not in data:
        data['isApproved'] = False

    if 'isHighlighted' not in data:
        data['isHighlighted'] = False

    if 'isEdited' not in data:
        data['isEdited'] = False

    if 'isSpam' not in data:
        data['isSpam'] = False

    if 'isDeleted' not in data:
        data['isDeleted'] = False

    db = DBconnect.connect()
    cur = db.cursor()
    try:
        cur.execute("""INSERT INTO post (date, thread, message, user, forum, parent,
                                     isApproved, isHighlighted, isEdited, isSpam, isDeleted)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (data['date'], data['thread'], data['message'], data['user'], data['forum'],
                    data['parent'], int(data['isApproved']), int(data['isHighlighted']), int(data['isEdited']),
                    int(data['isSpam']), int(data['isDeleted']),))
        post = cur.lastrowid
        db.commit()
    except Exception as e:
        db.rollback()
        cur.close()
        db.close()
        raise e

    cur.close()

    cur = db.cursor()
    cur.execute("""UPDATE thread
                   SET posts = posts + 1
                   WHERE id = %s""", (data['thread'],))
    db.commit()
    cur.close()

    cur = db.cursor()
    cur.execute("""SELECT id, date, forum, isApproved, isDeleted, isEdited,
                   isHighlighted, isSpam, message, thread, user
                   FROM post
                   WHERE id = %s""", (post,))
    post = cur.fetchone()
    cur.close()
    db.close()

    post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")
    return post


def details(db=0, close_db=True, **data):
    required(data, ['post'])
    if db == 0:
        db = DBconnect.connect()
    cur = db.cursor()
    cur.execute("""SELECT * FROM post
                   WHERE id = %s""", (data['post'],))
    post = cur.fetchone()
    cur.close()
    post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")
    if 'related' in data:
        if 'user' in data['related']:
            post['user'] = user.details(db, False, **post)
        if 'thread' in data['related']:
            post['thread'] = thread.details(db, False, **post)
        if 'forum' in data['related']:
            short_name = {'forum': post['forum']}
            post['forum'] = forum.details(db, False, **short_name)
    if close_db:
        db.close()
    return post


def list(**data):

    check_optional_param(data, 'order', 'desc')
    if 'order' not in data:
        data['order'] = 'desc'
    if 'thread' not in data and 'forum' not in data:
        raise Exception("thread or forum is required")
    if 'thread' in data and 'forum' in data:
        raise Exception("choose either thread or forum")

    query = StringToFile.StringToFilefunc()
    params = ()

    if 'thread' in data:
        query.append("""SELECT * FROM post
                       WHERE thread = %s""")
        params += (data['thread'],)
    elif 'forum' in data:
        query.append("""SELECT * FROM post
                       WHERE forum = %s""")
        params += (data['forum'],)

    if 'since' in data:
        query.append(""" AND date >= %s""")
        params += (data['since'],)

    query.append(""" ORDER BY date %s""" % data['order'])
    if 'limit' in data:
        query.append(""" LIMIT %s""" % data['limit'])

    db =DBconnect.connect()
    cur = db.cursor()
    cur.execute(str(query), params)
    posts = cur.fetchall()
    cur.close()
    db.close()

    for post in posts:
        post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")

    return posts


def remove(**data):
    required(data, ['post'])
    db = DBconnect.connect()
    cur = db.cursor()
    try:
        cur.execute("""UPDATE post
                       SET isDeleted = 1
                       WHERE id = %s""", (data['post'],))
        db.commit()
    except Exception as e:
        db.rollback()
        cur.close()
        db.close()
        raise e
    cur.close()
    db.close()
    return {'post': data['post']}


def restore(**data):
    required(data, ['post'])
    db = DBconnect.connect()
    cur = db.cursor()
    try:
        cur.execute("""UPDATE post
                       SET isDeleted = 0
                       WHERE id = %s""", (data['post'],))
        db.commit()
    except Exception as e:
        db.rollback()
        cur.close()
        db.close()
        raise e
    cur.close()
    db.close()
    return {'post': data['post']}


def update(**data):
    required(data, ['post', 'message'])
    db = DBconnect.connect()
    cur = db.cursor()
    try:
        cur.execute("""UPDATE post
                       SET message = %s
                       WHERE id = %s""", (data['message'], data['post'],))
        db.commit()
    except Exception as e:
        db.rollback()
        cur.close()
        db.close()
        raise e
    cur.close()
    post = details(db, True, **data)
    return post


def vote(**data):
    required(data, ['post', 'vote'])
    data['vote'] = int(data['vote'])
    if data['vote'] != -1 and data['vote'] != 1:
        raise Exception("Illegal vote.")
    db = DBconnect.connect()
    cur = db.cursor()
    try:
        if data['vote'] == -1:
            cur.execute("""UPDATE post
                           SET dislikes = dislikes + 1,
                               points = points - 1
                           WHERE id = %s""", (data['post'],))
        else:
            cur.execute("""UPDATE post
                           SET likes = likes + 1,
                               points = points + 1
                           WHERE id = %s""", (data['post'],))
        db.commit()
    except Exception as e:
        cur.close()
        db.rollback()
        db.close()
        raise e
    cur.close()
    post = details(db, True, **data)
    return post

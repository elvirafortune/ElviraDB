__author__ = 'Elvira'

from database import  DBconnect
from SubscriptionsList import *
from StringToFile import *

def Followerin(data, mode, db=DBconnect.connect()):
    cur = db.cursor()
    cur.execute("""SELECT * FROM user
                   WHERE email = %s""", (data['user'],))
    user = cur.fetchone()
    cur.close()
    if not user or len(user) == 0:
        raise Exception('such user doesnt exist')
    query = StringToFilefunc()
    params = ()
    if mode[1] == 'long':
        query.append("""SELECT *""")
    else:
        query.append("""SELECT email""")

    query.append(""" FROM user
                  WHERE email in (SELECT follower
                  FROM followers
                  WHERE followee = %s AND isFollowing = 1)""")
    params += (user['email'],)
    if 'since_id' in data:
        query.append(""" AND id >= %s""")
        params += (data['since_id'],)
    if mode[1] == 'long':
        query.append(""" ORDER BY name %s""" % data['order'])
    if 'limit' in data:
        query.append(""" LIMIT %s""" % data['limit'])

    cur = db.cursor()
    cur.execute(str(query), params)
    if mode[1] == 'long':
        users = cur.fetchall()
        for user in users:
            user['subscriptions'] = SubscriptionsListfunc(user['email'], db)
            temp = {'user' : user['email']}
            user['followers'] = Followerin(temp, ['followers', 'short'], db)

            user['following'] = Followerfrom(temp, ['followees', 'short'], db)
    else:
        temp = cur.fetchall()
        users = []
        for user in temp:
            users.append(user['email'])
    cur.close()
    return users

def Followerfrom(data, mode, db=DBconnect.connect()):
    cur = db.cursor()
    cur.execute("""SELECT * FROM user
                   WHERE email = %s""", (data['user'],))
    user = cur.fetchone()
    cur.close()
    if not user or len(user) == 0:
        raise Exception('such user doesnt exist')
    query = StringToFilefunc()
    params = ()
    if mode[1] == 'long': #change this!!
        query.append("""SELECT *""")
    else:
        query.append("""SELECT email""")

    query.append(""" FROM user
                  WHERE email in (SELECT followee
                    FROM followers
                    WHERE follower = %s AND isFollowing = 1)""")
    params += (user['email'],)
    if 'since_id' in data:
        query.append(""" AND id >= %s""")
        params += (data['since_id'],)
    if mode[1] == 'long':
        query.append(""" ORDER BY name %s""" % data['order'])
    if 'limit' in data:
        query.append(""" LIMIT %s""" % data['limit'])

    cur = db.cursor()
    cur.execute(str(query), params)
    if mode[1] == 'long':
        users = cur.fetchall()
        for user in users:
            user['subscriptions'] = SubscriptionsListfunc(user['email'], db)
            temp = {'user' : user['email']}
            user['following'] = Followerfrom(temp, ['followees', 'short'], db)

            user['followers'] = Followerin(temp, ['followers', 'short'], db)
    else:
        temp = cur.fetchall()
        users = []
        for user in temp:
            users.append(user['email'])
    cur.close()
    return users
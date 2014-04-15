__author__ = 'Elvira'


def SubscriptionsListfunc(user, db):

    cur = db.cursor()
    cur.execute("""SELECT thread
                   FROM subscription
                   WHERE user = %s AND isSubscribed = 1""", (user,))
    temp_subscriptions = cur.fetchall()
    subscriptions = []
    for subscription in temp_subscriptions:
            subscriptions.append(subscription['thread'])
    cur.close()

    return subscriptions



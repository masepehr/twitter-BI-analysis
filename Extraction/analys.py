from twdata.models import Persons,Tweets
def analys_person(uname):
    person=Persons.objects.filter(uname=uname)[0]
    # return [t.likes_count for t in person.tweets.all()],[t.date for t in person.tweets.all()]
    return list(person.tweets.all())
import redis


r = redis.Redis(host='localhost', port=6379, db=0, protocol=3)

r.set('foo', 'bar')


print(r.get('foo'))
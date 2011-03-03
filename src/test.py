import linkedlistredis as llr
import time

r=llr.LinkedListRedis()
r.set('foo','bar', 11)
r.set('mus','tafa', 1)
r.set('hel','lo', 1)
r.set('he1','lo', 6)
r.set('he2','lo', 15)
r.set('he3','lo', 1)
r.set('he4','lo', 1)
print "Initial list: "
r.stats()

time.sleep(2)

# get 'he4' and clean linked list while traversing
r.get('he4')
r.stats()

# kill all 3 remaining nodes one by one
# order: first, third, second
r.dele('foo')
r.stats()
r.dele('he2')
r.stats()
r.dele('he1')
r.stats()


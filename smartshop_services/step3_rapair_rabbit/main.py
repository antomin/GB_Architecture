import random
import time
import redis

while True:
    with redis.Redis(host='redis', port=6379, decode_responses=True) as redis_client:
        print('Queue waiting...')
        phone = redis_client.brpop(['repair'])
        repair_time = random.randint(3, 20)
        print('rep_time', repair_time)
        time.sleep(repair_time)
        print('Work is done!')

        requests.post('http://orders:5000/change/', data={'phone': phone[1], 'status': 'DONE'})

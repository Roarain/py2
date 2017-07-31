import random
import string

class GenerateRandom(object):
    def __init__(self):
        self.quantity = random.randint(8,12)

    def gen_random(self):
        letters = string.ascii_letters
        nums = string.digits
        results = letters + nums
        result = [random.choice(results) for i in range(self.quantity)]
        return ''.join(result)
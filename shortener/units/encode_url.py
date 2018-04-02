import math
import hashlib


def encode_url(url, step=8):
    url_encode = url.encode(encoding='UTF-8')
    hash = hashlib.sha256(url_encode).hexdigest()
    hash_split = [hash[a:a+step] for a in range(0, 64, step) if a+step < 64]
    width = math.ceil(math.log(math.pow(16, step), 62))

    hashed = []
    for hash in hash_split:
        hash_num = int(hash, 16)
        hash_base62_list = []
        while hash_num != 0:
            num = hash_num % 62

            if num < 10:
                char = chr(ord('0')+num)
            elif num < 36:
                char = chr(ord('a')+num-10)
            else:
                char = chr(ord('A')+num-36)

            hash_base62_list.append(char)
            hash_num //= 62
        hash_base62_list.reverse()

        hash_base62_string = ''.join(hash_base62_list)
        hash_base62_string = hash_base62_string.zfill(width)
        hashed.append(hash_base62_string)

    return hashed
fruits = ['사과','배','배','감','수박','귤','딸기','사과','배','수박']

def fruit(target):
    count = 0
    for fruit in fruits:
        if fruit == '사과':
            count += 1
    return count

subak_count = fruit('수박')
print(subak_count)

sagwa_count = fruit('사과')
print(sagwa_count)
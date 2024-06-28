people = [{'name': 'bob', 'age': 20}, 
          {'name': 'carry', 'age': 38},
          {'name': 'john', 'age': 7},
          {'name': 'smith', 'age': 17},
          {'name': 'ben', 'age': 27}]

def get_age(name):
    for person in people:
        if person['name'] == name:
            return person['age']
    return '이름을 확인해주세요'

carry_age = get_age('carry')
print(carry_age)
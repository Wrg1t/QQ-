from random import randint

def aba():
    l = ['阿巴','?','!']
    li = []
    for i in range(4):
        index = randint(0, 2)
        li.append(l[index])
    if not '阿巴' in li:
        li.append('阿巴')
        return ''.join(i for i in li)
    else:
        return ''.join(i for i in li)
    
if __name__ == "__main__":
    print(aba())
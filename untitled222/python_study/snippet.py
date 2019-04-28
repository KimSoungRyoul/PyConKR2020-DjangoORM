from django.utils.functional import cached_property


class ASDF(object):
    aaa = 2

    @cached_property
    def bbb(self):
        return self.aaa + 1


import weakref

a_set = {0, 1}
wref = weakref.ref(a_set)
print(wref)
print(wref())
print(a_set)

print('여전히 존재: ', wref())

print(wref() is None)

print(wref() is None)

a = [1, 2, 3, ]
b = a.append(4)
b

charles = {'name': 'asdf', 'num': 123}


# 가변 객체와 불가변 객체의 차이
l1 = [1, 2, ]
print(id(l1))
l1 += [3, 4]
print(id(l1))

t1 = (1, 2,)
print(id(t1))
t1 += (3, 4,)
print(id(t1))


a_param=[1,2,3]
b_param=(1,2,)
print(id(a_param))
print(id(b_param))
def hi(lll, t1):
    print(id(lll), id(t1))

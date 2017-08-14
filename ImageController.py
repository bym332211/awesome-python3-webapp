from test import MyTest

def test():
    item1 = MyTest('')
    item1.color = "test1"
    item1.__name = 'item1'

    item2 = MyTest('')
    item2.color = "test2"

    print(item1.color, item2.color)
    print(item1.__name, item2.__name)

test()
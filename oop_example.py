# Inheritance

class Parent:
    def __init__(self) -> None:
        self.example = True
    
    def greetings(self):
        print('hi')

class Child(Parent):
    pass

child = Child()
print(child.example)
child.greetings()

# Overwriting (Polymorphism)

from PIL import Image

class Dataset:
    def __init__(self, data):
        self.data = data

    def count_examples(self):
        print(len(self.data))

    def show_first_example(self):
        print(self.data[0])

class ImnageDataset(Dataset):
    def show_first_example(self):
        with Image.open(self.data[0]) as img:
            img.show()

dataset = Dataset([1,2,3])
dataset.show_first_example()

# image_dataset = ImageDataset(['images/shark.webp','images/dog.jpg','images/frog.jpg'])
# image_dataset.show_first_example()

# Super class

class Device:
    def __init__(self):
        self.on = False
    
    def toggle_power(self):
        self.on = not self.on
        if self.on:
            print('Power on')
        else:
            print('Power off')

            
class Mouse(Device):
    def __init__(self):
        super().__init__()

    def move(self):
        print('Wiggle')

        
class Computer(Device):
    def __init__(self):
        super().__init__() # use super() method to access methods of the parent
        self.browser = 'safari'

    def open_browser(self):
        try:
            assert self.on
            print(f"The browser {self.browser} was opened")
        except:
            print("Turn me on first")

            
class Laptop(Computer):
    def __init__(self):
        super().__init__()

        
# run example 
my_mouse = Mouse()        

my_laptop = Laptop()
my_laptop.open_browser()
my_laptop.toggle_power()
my_laptop.open_browser()
my_laptop.toggle_power()

# Polymorthism (once more), inheriting empty methods

class Model():
    def __init__(self):
        # defien stuff that is suseful for all kind of models
        pass

    def predict(self):
        raise NotImplementedError('You need to define this method')


class NauralNetworkModel(Model):
    def predict(self):
        # make prediction
        print("a")
        return self
    
class LinearRegressionModel():
    def predict(self):
        # make prediction
        print("b")
        return self
    
nn = NauralNetworkModel()
linear_regression = LinearRegressionModel()

# same name of method, different behaviour
nn.predict()
linear_regression.predict()

# loop over models
models = [nn, linear_regression]
for model in models:
    model.predict() # same name of method, instances of different classes

# Mixin
# A mixin is a class that provides methods to other classes but are not considered a base class. 
    
class SpeakMixin:
    def speak(self):
        name = self.__class__.__name__.lower()
        print(f'The {name} says: "hello... I mean... woof!"')


class RollOverMixin:
    def roll_over(self):
        print('Look at me, I am rolling!')


class Dog(RollOverMixin, SpeakMixin):
    pass

class Cat(SpeakMixin):
    pass

jake = Dog()
jake.speak()
jake.roll_over()
    
# Encapsulation
class Database:
    def get_data(self):
        # code to get dat from database
        print('getting data from database')
        pass

    def insert_data(self, data):
        print('inserting data into database')
        pass


class Preprocessor:
    def remove_duplicata_data(self, data):
        # code to clean data
        print('remove duplicates')
        pass

    def remove_rows_with_missing_values(self, data):
        # code to remove rows
        print('remove rowas with missing data')
        pass

database = Database()
preprocessor = Preprocessor()

data = database.get_data()
data = preprocessor.remove_duplicata_data(data)
data = preprocessor.remove_rows_with_missing_values(data)
database.insert_data(data)

# Note: In python, there are no 'protected' and 'private' methods - these are just conventions.
# If method name is preceeded by a single dash - it is 'protected', and should not be changed
# If it is preceded by double-dash - it is 'private' and shoudl only be called form within the class

# Mixin class for 'private' methods
class AsDictMixin:

    def to_dict(self):

        # list attributes: non-callable, non-private, non-protected
        attribute_list = [a for a in dir(self) if not callable(getattr(self, a)) and not a.startswith('__') and not self._is_protected(a)]
        attribute_list = sorted(attribute_list)

        # populate a dict
        d=dict()
        for a in attribute_list :
            d[a] = self.__getattribute__(a)

        return d

    def _represent(self, value):
        if isinstance(value, object):
            if hasattr(value, 'to_dict'):
                return value.to_dict()
            else:
                return str(value)
        else:
            return value

    def _is_protected(self, prop):
        return prop.startswith('_')


class Person(AsDictMixin):
    def __init__(self, name, address, salary):
        self.name = name
        self.address = address
        self._salary = salary

ivan = Person('Ivan', 'London', '100000000')
d = ivan.to_dict()

print(d)


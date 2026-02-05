# Example 2/4: MayBe with objects
from dataclasses import dataclass
from nofuture import MayBe


# Focus: mapping objects through MayBe
@dataclass
class Dog:
    name: str

    def speak(self) -> str:
        return f"{self.name} howls: WOOF!"


@dataclass
class Cat:
    name: str

    def speak(self) -> str:
        return f"{self.name} hisses: MROOOW!"


# Keep the example obvious and non-magical
ROSTER = {
    "Larsen": Dog,
    "Romy": Dog,
    "Whiskers": Cat,
    "Mina": Cat,
}


def pick_animal(name: str) -> MayBe:
    """Pick a known animal from the roster, otherwise Nothing."""
    cls = ROSTER.get(name)
    if cls is None:
        return MayBe.nothing()
    return MayBe.just(cls(name))


maybe_dog = pick_animal("Larsen")
maybe_cat = pick_animal("Whiskers")

greeting1 = maybe_dog.map(lambda a: a.speak())
greeting2 = maybe_cat.map(lambda a: a.speak())

assert repr(greeting1) == "Just(Larsen howls: WOOF!)"
assert repr(greeting2) == "Just(Whiskers hisses: MROOOW!)"

# Fallback value with or_else
default_cat = Cat("FallbackCat")
final_greeting = greeting2.or_else(default_cat.speak())
assert final_greeting == "Whiskers hisses: MROOOW!"


# Chaining with >> and a MayBe-returning function


def to_upper(msg: str) -> MayBe:
    return MayBe.just(msg.upper())


chained = greeting1 >> (lambda msg: to_upper(msg))
assert repr(chained) == "Just(LARSEN HOWLS: WOOF!)"


# Pattern matching with objects
def describe_animal(maybe_animal: MayBe) -> str:
    return maybe_animal.match(just=lambda a: f"Found: {a.speak()}", nothing=lambda: "No animal found")


assert describe_animal(maybe_dog) == "Found: Larsen howls: WOOF!"
assert describe_animal(maybe_cat) == "Found: Whiskers hisses: MROOOW!"

# to_option for integration with existing code
animal_or_none = maybe_dog.to_option()
assert animal_or_none is not None
assert animal_or_none.name == "Larsen"

print("MayBe objects OK - alley cats approved")

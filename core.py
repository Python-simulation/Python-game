# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 10:51:59 2020

@author: jonathan
"""
import pickle

import weakref


class Character:

    _instances = set()

    def __init__(self, dict_init=dict(), **kwargs):
        """kwargs allows to change the default value of any variable name.
        Must protect some variable to avoid cheating ??"""
        self._instances.add(weakref.ref(self))

        dict_default = {
            "name": "NPC",
            "stats": {"health_max": 100},
            "inventory": {"money": Money(), "potion": Potion()},
            "body": {"weapon": None},
            "fists": Weapon(),
        }

        self.__dict__ = dict(
            list(self.__dict__.items())
            + list(dict_default.items())
            + list(dict_init.items())
            + list(kwargs.items())
            )

        self.health = self.stats["health_max"]

    @classmethod
    def getinstances(cls):

        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    @property  # Character.health call this function instead
    def health(self):
        # print("property of", self.name)
        return self.__health_value

    @health.setter  # Character.health = x call this function instead
    def health(self, value):
        # print("setter for", self.name)
        self.__health_value = value

        if self.__health_value <= 0:
            self.dead()

    def pick_item(self, item):
        # TODO: change name en id ou nom class pour etre unique sinon remplace arme existante par nouvelle
        self.inventory[id(item)] = item
        remove_item_from_world(item)
        print(item.name, "added to the inventory")

    def drop_item(self, item):
        # TODO: change name en id ou nom class pour etre unique sinon remplace arme existante par nouvelle

        if item not in self.inventory.values():
            print("The item", item.name, "isn't in the inventory")
            return

        try:
            self.inventory.pop(item.id) # TODO: ugly to use two different var for different object
        except AttributeError:
            self.inventory.pop(item.name)

        add_item_to_world(item)
        print(item.name, "drop to the floor")

    def equip_from_inventory(self, element, location):

        if element is None:
            print("no weapon choosen")
            return

        if location not in self.body:
            print("The location", location, "doesn't exist")
            return

        elif element.id in self.inventory:  # should not occure if player can only choose element from inventory having id (must not equipped class without id like money or potion)

            if self.body[location] is not None:
                self.move_item_from_body_to_inventory(location)

            self.inventory.pop(element.id)
            self.body[location] = element
            print(self.name, "equip", element.name, "as", location)

        else:
            print("try to remove a item that don't exist in the inventory")

    def move_item_from_body_to_inventory(self, element_name):

        if element_name not in self.body:
            print("The element", element_name, "isn't equipped")
            return

        try:
            item_name = self.body[element_name].id  # change to id
        except AttributeError:
            print("nothing equipped as", element_name)
            return

        self.inventory[item_name] = self.body[element_name]

        self.body[element_name] = None

#        if element_name == "weapon":
#            self.body[element_name] = Weapon()

        print(self.name, "move", element_name, "to the inventory")

    def attack(self, target):
        weapon = self.body.get("weapon", None)

        if weapon is None:
            weapon = self.fists

        print(self.name, "attacks with", weapon.name, "doing",
              weapon.damage, "damages to", target.name)
        target.health -= weapon.damage
        print(target.name, "health:", target.health,
              "/", target.stats["health_max"])

    def dead(self):
        self.__health_value = 0
        print(self.name, "is dead !")
        self.attack = empty_func
        self.equip = empty_func
        self.pick_item = empty_func
        self.equip_from_inventory = empty_func
        self.equip = empty_func

        for item_name in dict(self.body):
            self.move_item_from_body_to_inventory(item_name)

        for item in dict(self.inventory):
            self.drop_item(self.inventory[item])

        for instance in Character.getinstances():

            if self is instance:
                print("should delete", instance)
                del instance  #TODO: can't find how to do it, should we do it ?

    def choose_weapon_temp(self):
        for item in self.inventory.values():
            choice = item.__dict__.get("id", None)
#            print(choice)
            if choice is not None:
                return choice
        return None


class Potion:
    def __init__(self, value=0):
        self.name = "potion"
        self.healing = value

    def use(self):
        ""


class Money:
    def __init__(self, value=0):
        self.name = "money"
        self.money = value


def empty_func(*args, **kwargs):
    ""


class empty_class:
    def __init__(self):
        self.name = None


class Weapon:
    def __init__(self, Weapon_Type=None, **kwargs):
        self.id = id(self)  # Change when open file
        # -> #TODO: can be problematic if new weapon has same id as self.id
        # possible solution: settting id to id=name+id(self) to reduce the probability
        self.name = "fists"  # default values
        self.damage = 1
        self.for_all_weapon = 1

#        print(Weapon_Type, kwargs)
#        Weapon_Type.__init__(self, **kwargs)  # specific values of the type of weapon


class Knife:
    def __init__(self, dict_init=dict(), **kwargs):

        Weapon.__init__(self)  # specific values of the type of weapon

        dict_default = {
            "name": "hunting knife",
            "damage": 20,
            "specific_to_weapon": 2,
        }

        self.__dict__ = dict(
            list(self.__dict__.items())
            + list(dict_default.items())
            + list(dict_init.items())
            + list(kwargs.items())
            )
#        print("final", self.__dict__)


class Riffle:
    def __init__(self, dict_init=dict(), **kwargs):

        Weapon.__init__(self)  # specific values of the type of weapon

        dict_default = {
            "name": "riffle",
            "damage": 50,
        }
#        print("dict_default", dict_default)
#        print("dict_init", dict_init)
#        print("kwargs", kwargs)
        self.__dict__ = dict(
            list(self.__dict__.items())
            + list(dict_default.items())
            + list(dict_init.items())
            + list(kwargs.items())
            )
#        print("final", self.__dict__)


def remove_item_from_world(item):
    print(item.name, "must be removed from world: not implemented yet")


def add_item_to_world(item):
    print(item.name, "must be added to world: not implemented yet")


def save_data(file, data):

    with open(file, "wb") as f:
        f.write(pickle.dumps(data))
    print("data of", data.name, "save in file", file)  # warning, data could not have .name


def load_data(file):

    with open(file, "rb") as f:
        data = pickle.loads(f.read())

    if isinstance(data, Character):
        data._instances.add(weakref.ref(data))  # needed for character

    print("data from file", file, "openned")
    return data

# =============================================================================
# Beginning of game
# =============================================================================

me = Character(name="John")  # act as kwargs

me.pick_item(Riffle(damage=100))  # not good to have riffle by itself and not from weapon -> should be a method of class weapon

#me.pick_item(Riffle())

choice = me.choose_weapon_temp()
me.equip_from_inventory(me.inventory.get(choice, None), "weapon")

#choice = me.choose_weapon_temp()
#me.equip_from_inventory(me.inventory.get(choice, None), "weapon")

#me.move_item_from_body_to_inventory("weapon")

enemy_param = {
    "name": "Evil Communist",
    "stats": {"health_max": 200},
    "inventory": {"money": Money(100)},
    "body": {"weapon": Knife()}
}

enemy = Character(enemy_param)  # act as dict_init and not kwargs

print("")

me.attack(enemy)
enemy.attack(me)

me.attack(enemy)
enemy.attack(me)
#
#me.attack(enemy)
#enemy.attack(me)
#
#me.attack(enemy)
#enemy.attack(me)  # do nothing as expected but temporary
#
##me.attack(enemy)  # should not be possible -> must del enemy from inside (can't do)
#
#
print("")
save_data("character.dat", me)

me = load_data("character.dat")
#
print("liste instance character")
for obj in Character.getinstances():
    print ("\t",obj.name) # prints "John", "Evil Communist"

#for item in me.inventory.values():
#    print(item.__dict__.get("id", None))

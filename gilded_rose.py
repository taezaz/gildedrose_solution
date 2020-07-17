# -*- coding: utf-8 -*-

class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update(self, days=1):
        while days > 0:
            days -= 1

            for item in self.items:
                item.update()


# NOTE: Another potential implementation that would de-couple
# Item from it's update logic would be to have a separate class
# ItemUpdater which would accept Item when instantiated.
# ItemUpdater could be added to items list, same as Item
# In GildedRose there would be another attribute self.updaters.
# If item was added to items list without being wrapped in an
# updater, then it would be assigned the default one.
# GildedRose would work like this (pseudo-magic-code!):
# __init__:
#     self.items = [
#         i.item if isinstance(upd, ItemUpdater) else i
#         for i in items
#     ]
#     self.updaters = group_dict(updater_cls, updater_items)
#     self.updaters[default_cls] = unwrapped_items
# update:
#     for updater_cls, items in self.updaters.iteritems():
#         updater_cls(item).update()
class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class ItemWrapped(Item):
    def __init__(self, name, sell_in, quality):
        if sell_in < 0:
            raise Exception(
                'Cannot add expired items to inventory'
            )

        # Using old-style super, because task description
        # mentions that Item cannot be touched
        Item.__init__(self, name, sell_in, quality)
        self.quality = min(self.quality, 50)

    def update(self):
        self._update_sell_in()
        self._update_quality()

        if self.quality < 0:
            self.quality = 0
        if self.quality > 50:
            self.quality = 50

    def _update_sell_in(self):
        self.sell_in -= 1

    def _update_quality(self):
        raise NotImplementedError


class ItemStatic(ItemWrapped):
    def _update_sell_in(self):
        pass

    def _update_quality(self):
        pass


class ItemRegular(ItemWrapped):
    def _update_quality(self):
        self.quality -= 1
        if self.sell_in < 0:
            self.quality -= 1


class ItemConjured(ItemWrapped):
    # NOTE: Could be done more DRY by having a class attribute
    # `quality_decrement` which would be set as:
    # ItemRegular:
    #     quality_decrement = 1
    # ItemConjured(ItemRegular):
    #     quality_decrement = 2
    # ItemAgedBrie(ItemRegular):
    #     quality_decrement = -1
    def _update_quality(self):
        self.quality -= 2
        if self.sell_in < 0:
            self.quality -= 2


class ItemAgedBrie(ItemWrapped):
    def _update_quality(self):
        self.quality += 1
        if self.sell_in < 0:
            self.quality += 1


class ItemBackstagePass(ItemWrapped):
    def _update_quality(self):
        if self.sell_in < 0:
            self.quality = 0
            return

        self.quality += 1
        if self.sell_in <= 10:
            self.quality += 1
        if self.sell_in <= 5:
            self.quality += 1

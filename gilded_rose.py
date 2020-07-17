# -*- coding: utf-8 -*-

class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update(self, days=1):
        while days > 0:
            days -= 1

            for item in self.items:
                item.update()


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

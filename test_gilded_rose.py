# -*- coding: utf-8 -*-

import unittest

from gilded_rose import (
    GildedRose,
    ItemRegular,
    ItemStatic,
    ItemConjured,
    ItemAgedBrie,
    ItemBackstagePass,
)


class GildedRoseTest(unittest.TestCase):
    def test_regular_item(self):
        item = ItemRegular(
            "Corn", sell_in=10, quality=10,
        )

        rose = GildedRose([item])
        rose.update()
        self.assertEqual(
            item.sell_in, item.quality, 9,
        )

        rose.update(days=9)
        self.assertEqual(
            item.sell_in, item.quality, 0,
        )

        rose.update(days=100)
        self.assertEqual(item.sell_in, -100)
        self.assertEqual(item.quality, 0)

    def test_static_item(self):
        item = ItemStatic(
            "Sulfuras", sell_in=10, quality=9000,
        )

        GildedRose([item]).update(days=100)
        self.assertEqual(item.sell_in, 10)
        self.assertEqual(item.quality, 50)

    def test_conjured_item(self):
        item = ItemConjured(
            "Sword", sell_in=20, quality=100,
        )

        rose = GildedRose([item])
        rose.update()
        self.assertEqual(item.sell_in, 19)
        self.assertEqual(item.quality, 48)

        rose.update(days=19)
        self.assertEqual(item.sell_in, 0)
        self.assertEqual(item.quality, 10)

        rose.update()
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 6)

    def test_brie_item(self):
        item = ItemAgedBrie(
            "Cheese", sell_in=10, quality=5,
        )

        rose = GildedRose([item])
        rose.update()
        self.assertEqual(item.sell_in, 9)
        self.assertEqual(item.quality, 6)

        rose.update(days=9)
        self.assertEqual(item.sell_in, 0)
        self.assertEqual(item.quality, 15)

        rose.update()
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 17)

    def test_backstage_pass_item(self):
        item = ItemBackstagePass(
            "Backstage Pass", sell_in=20, quality=10,
        )

        rose = GildedRose([item])
        rose.update()
        self.assertEqual(item.sell_in, 19)
        self.assertEqual(item.quality, 11)

        rose.update(days=8)
        self.assertEqual(item.sell_in, 11)
        self.assertEqual(item.quality, 19)

        rose.update()
        self.assertEqual(item.sell_in, 10)
        self.assertEqual(item.quality, 21)

        rose.update(days=4)
        self.assertEqual(item.sell_in, 6)
        self.assertEqual(item.quality, 29)

        rose.update()
        self.assertEqual(item.sell_in, 5)
        self.assertEqual(item.quality, 32)

        rose.update(days=100000)
        self.assertEqual(item.sell_in, -99995)
        self.assertEqual(item.quality, 0)


if __name__ == '__main__':
    unittest.main()

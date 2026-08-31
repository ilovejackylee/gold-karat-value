import unittest

from gold_karat_value import CalcError, melt_value, purity_ratio, scrap_value, to_grams


class GoldKaratValueTest(unittest.TestCase):
    def test_fourteen_karat_ratio(self):
        self.assertAlmostEqual(purity_ratio(14), 14 / 24, places=12)

    def test_melt_value_matches_cent_rounding(self):
        value = melt_value(10, "gram", 14, 65)
        self.assertEqual(value.per_gram, 37.92)
        self.assertEqual(value.total, 379.20)
        self.assertEqual(value.per_troy_ounce, 1179.44)
        self.assertEqual(value.per_troy_pound, 14153.34)

    def test_troy_ounce_converts_to_grams(self):
        self.assertAlmostEqual(to_grams(1, "troy_ounce"), 31.1035, places=12)

    def test_scrap_applies_discount(self):
        value = scrap_value(10, "gram", 14, 65, 0.85)
        self.assertEqual(value.market, 379.20)
        self.assertEqual(value.scrap, 322.32)

    def test_rejects_out_of_range_karat(self):
        with self.assertRaises(CalcError):
            melt_value(1, "gram", 25, 10)


if __name__ == "__main__":
    unittest.main()

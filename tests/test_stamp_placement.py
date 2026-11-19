import unittest

import pymupdf

from scripts.stamp import get_stamp_rect


class StampPlacementTests(unittest.TestCase):
    def test_position_and_scale_control_stamp_rectangle(self):
        page = pymupdf.Rect(0, 0, 600, 800)

        stamp_rect, scale = get_stamp_rect(
            page,
            100,
            50,
            {"x": 50, "y": 25, "scale": 200},
        )

        self.assertEqual(stamp_rect, pymupdf.Rect(200, 175, 400, 275))
        self.assertEqual(scale, 200)

    def test_stamp_position_is_clamped_to_page_edges_by_percentage(self):
        page = pymupdf.Rect(0, 0, 600, 800)

        stamp_rect, _ = get_stamp_rect(
            page,
            100,
            50,
            {"x": 100, "y": 100, "scale": 100},
        )

        self.assertEqual(stamp_rect, pymupdf.Rect(500, 750, 600, 800))

    def test_invalid_position_or_scale_is_rejected(self):
        page = pymupdf.Rect(0, 0, 600, 800)

        for placement in (
            {"x": 101, "y": 50, "scale": 100},
            {"x": 50, "y": 50, "scale": 301},
        ):
            with self.subTest(placement=placement):
                with self.assertRaises(ValueError):
                    get_stamp_rect(page, 100, 50, placement)


if __name__ == "__main__":
    unittest.main()

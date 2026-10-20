import unittest

from main import Appoinment, appointments, create_appointment


class AppointmentTests(unittest.TestCase):
    def setUp(self):
        appointments.clear()

    def test_creates_objects_and_saves_two_records(self):
        first = create_appointment("Иванова А.А.", 1, 1, "10:00")
        second = create_appointment("Петрова А.А.", 1, 1, "11:00")
        self.assertIsInstance(first, Appoinment)
        self.assertIsInstance(second, Appoinment)
        self.assertEqual([item.client_name for item in appointments],
                         ["Иванова А.А.", "Петрова А.А."])
        self.assertEqual([item.time for item in appointments], ["10:00", "11:00"])

    def test_required_fields(self):
        invalid = [
            ("", 1, 1, "12:00"),
            ("   ", 1, 1, "12:00"),
            ("Иванова", 0, 1, "12:00"),
            ("Иванова", 1, 0, "12:00"),
            ("Иванова", 1, 1, ""),
            ("Иванова", 100, 1, "12:00"),
            ("Иванова", 1, 100, "12:00"),
        ]
        for params in invalid:
            with self.subTest(params=params):
                self.assertIsNone(create_appointment(*params))
        self.assertEqual(appointments, [])

    def test_working_hours(self):
        for time in ["00:00", "07:59", "20:01", "23:59", "25:00", "12:61", "8:00", "hello"]:
            with self.subTest(time=time):
                self.assertIsNone(create_appointment("Клиент", 1, 1, time))
        self.assertEqual(len(appointments), 0)
        self.assertIsNotNone(create_appointment("Рано", 1, 1, "08:00"))
        self.assertIsNotNone(create_appointment("Поздно", 1, 1, "20:00"))

    def test_one_master_cannot_be_double_booked(self):
        self.assertIsNotNone(create_appointment("Первый", 1, 1, "10:00"))
        self.assertIsNone(create_appointment("Второй", 1, 2, "10:00"))
        self.assertEqual(len(appointments), 1)

    def test_different_masters_can_work_simultaneously(self):
        self.assertIsNotNone(create_appointment("Первый", 1, 1, "10:00"))
        self.assertIsNotNone(create_appointment("Второй", 2, 1, "10:00"))
        self.assertEqual(len(appointments), 2)


if __name__ == "__main__":
    unittest.main()

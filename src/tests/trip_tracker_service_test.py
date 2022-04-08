import unittest
from db_management import init_db
from entities.trip import Trip
from repositories.trip_repository import trip_repository
from repositories.profile_repository import profile_repository
from services.trip_tracker_service import trip_tracker_service


class TestTripTrackerService(unittest.TestCase):
    def setUp(self):
        init_db()
        profile_repository.add("Alice")
        profile_repository.add("Bob")
        trip_repository.add(1, "Test1_1", "2022-03-01 02:00",
                            "2022-03-02 15:28", 82800)
        trip_repository.add(1, "Test1_2", "2022-01-01 12:00",
                            "2022-01-01 15:28", 12800)

    def test_get_profiles(self):
        profiles = trip_tracker_service.get_profiles()
        self.assertEqual(len(profiles), 2)
        self.assertEqual(sorted([profile[1]
                         for profile in profiles]), ["Alice", "Bob"])

    def test_add_profile(self):
        profiles = trip_tracker_service.get_profiles()
        self.assertEqual(len(profiles), 2)
        self.assertEqual(sorted([profile[1]
                         for profile in profiles]), ["Alice", "Bob"])

        trip_tracker_service.add_profile("Charlie")
        trip_tracker_service.add_profile("Bob")

        profiles = trip_tracker_service.get_profiles()
        self.assertEqual(len(profiles), 3)
        self.assertEqual(sorted([profile[1] for profile in profiles]), [
            "Alice", "Bob", "Charlie"])

    def test_remove_profile(self):
        profiles = trip_tracker_service.get_profiles()
        self.assertEqual(len(profiles), 2)
        self.assertEqual(sorted([profile[1]
                         for profile in profiles]), ["Alice", "Bob"])

        trip_tracker_service.remove_profile(1)

        profiles = trip_tracker_service.get_profiles()
        self.assertEqual(len(profiles), 1)
        self.assertEqual(sorted([profile[1] for profile in profiles]), ["Bob"])

    def test_get_trips(self):
        trips_1 = trip_tracker_service.get_trips(1)
        trips_2 = trip_tracker_service.get_trips(2)
        self.assertEqual(len(trips_1), 2)
        self.assertEqual(len(trips_2), 0)
        self.assertEqual([trip.name for trip in trips_1],
                         ["Test1_2", "Test1_1"])
        trip_1 = trips_1[0]
        self.assertEqual(trip_1.name, "Test1_2")
        self.assertEqual(trip_1.duration, 12480)
        self.assertEqual(trip_1.length, 12800)
        self.assertEqual(trip_1.speed, 12800/12480)

    def test_add_trip(self):
        trips_1 = trip_tracker_service.get_trips(1)
        self.assertEqual(len(trips_1), 2)

        trip_tracker_service.add_trip(1, "Test1_3", "2021-03-01 02:00",
                                      "2021-03-02 15:28", 82800)

        trips_1 = trip_tracker_service.get_trips(1)
        self.assertEqual(len(trips_1), 3)

        trip_1 = trips_1[0]
        self.assertEqual(trip_1.name, "Test1_3")
        self.assertEqual(trip_1.duration, 134880)
        self.assertEqual(trip_1.length, 82800)
        self.assertEqual(trip_1.speed, 82800/134880)

    def test_remove_trip(self):
        trips_1 = trip_tracker_service.get_trips(1)
        self.assertEqual(len(trips_1), 2)

        trip_tracker_service.remove_trip(1)

        trips_1 = trip_tracker_service.get_trips(1)
        self.assertEqual(len(trips_1), 1)
        trip_1 = trips_1[0]
        self.assertEqual(trip_1.name, "Test1_2")

    def test_seconds_to_string(self):
        self.assertEqual(trip_tracker_service.seconds_to_string(0), "00:00:00")
        self.assertEqual(
            trip_tracker_service.seconds_to_string(20), "00:00:20")
        self.assertEqual(
            trip_tracker_service.seconds_to_string(60), "00:01:00")
        self.assertEqual(
            trip_tracker_service.seconds_to_string(3671), "01:01:11")
        self.assertEqual(
            trip_tracker_service.seconds_to_string(216069), "60:01:09")

    def test_valid_time(self):
        self.assertTrue(trip_tracker_service.valid_time("2022-01-03 12:00"))
        self.assertTrue(trip_tracker_service.valid_time("2022-01-03 12:00:50"))
        self.assertFalse(trip_tracker_service.valid_time("2022:01:03 02:00"))
        self.assertFalse(trip_tracker_service.valid_time("22-01-03 02:00"))
        self.assertFalse(trip_tracker_service.valid_time("2022-01-03 2:00"))
        self.assertFalse(trip_tracker_service.valid_time("2022-1-03 12:00:50"))
        self.assertFalse(trip_tracker_service.valid_time("2022-01-3 12:00:50"))
        self.assertFalse(trip_tracker_service.valid_time("2022-01-03 12"))
        self.assertFalse(trip_tracker_service.valid_time("2022-01-03 a2:00"))
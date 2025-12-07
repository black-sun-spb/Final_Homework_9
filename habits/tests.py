from django.test import TestCase
from users.models import User
from .models import Habit
from datetime import time


class HabitTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="habituser@example.com", password="pass")
        self.habit = Habit.objects.create(
            owner=self.user,
            action="Read 10 pages",
            time=time(hour=8),
            is_rewarding=False
        )

    def test_habit_str(self):
        self.assertEqual(str(self.habit), "Read 10 pages (useful)")

    def test_habit_creation(self):
        self.assertEqual(self.habit.owner, self.user)

    def test_habit_list_filter(self):
        """Проверка фильтров и булевых полей."""
        Habit.objects.create(owner=self.user, action="Run", time="08:00", is_rewarding=True, is_public=True)
        Habit.objects.create(owner=self.user, action="Sleep", time="22:00", is_rewarding=False, is_public=False)
        rewarding = Habit.objects.filter(is_rewarding=True)
        public = Habit.objects.filter(is_public=True)
        self.assertEqual(rewarding.count(), 1)
        self.assertEqual(public.count(), 1)


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.habit = Habit.objects.create(
            owner=self.user,
            place="Home",
            time="08:00",
            action="Read",
            is_rewarding=False,
        )

    def test_habit_str(self):
        self.assertEqual(str(self.habit), "Read (useful)")

    def test_cannot_have_reward_and_related_habit(self):
        habit_reward = Habit(
            owner=self.user,
            action="Run",
            time="09:00",
            reward="Coffee",
            related_habit=self.habit,
        )
        with self.assertRaises(Exception):
            habit_reward.full_clean()

    def test_public_habits_list(self):
        Habit.objects.create(
            owner=self.user, place="Park", time="10:00", action="Walk", is_public=True
        )
        public = Habit.objects.filter(is_public=True)
        self.assertTrue(public.exists())
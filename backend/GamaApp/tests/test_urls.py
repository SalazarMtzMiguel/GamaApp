from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import RunSimulationView, ViewSimulationResultsView


class UrlsTest(SimpleTestCase):
    def test_run_simulation_url(self):
        url = reverse('run_simulation', args=[1])
        self.assertEqual(resolve(url).func.view_class, RunSimulationView)

    def test_view_simulation_results_url(self):
        url = reverse('view_simulation_results', args=[1])
        self.assertEqual(resolve(url).func.view_class, ViewSimulationResultsView)

    def test_invalid_url(self):
        url = reverse('invalid_url', args=[1])
        with self.assertRaises(NoReverseMatch):
            resolve(url)
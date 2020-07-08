from django.test import TestCase

from products.forms import SearchForm


class SearchFormTest(TestCase):
    def test_max_length(self):
        form = SearchForm()
        self.assertEquals(form.fields["product"].max_length, 100)

    def test_random_data(self):
        user_input = "jambon"
        form = SearchForm(data={"product": user_input})
        self.assertTrue(form.is_valid())

"""Useful command to download and clean data from OpenFoodfact."""
import requests

keys = [
    "id",
    "product_name_fr",
    "nutrition_grade_fr",
    "url",
    "image_front_url",
    "image_ingredients_url",
]


class RequestData:
    """The class fetch the data and save it in to a json file."""

    def __init__(self):
        self.cat_url = "https://fr.openfoodfacts.org/categories.json"
        self.search_url = "https://fr.openfoodfacts.org/cgi/search.pl"
        self.list_cat = []
        self.list_prod = []
        self.data = {}

    def exec(self, page_size):
        """Main public function executing all necessary privates functions."""
        self.list_cat = self._fetch_category()
        data = self._fetch_products(page_size)
        return data

    def _fetch_category(self):
        """Request the list of category from the API."""
        print("Getting Categories from API")
        try:
            response = self._req(self.cat_url)
            data = response.json()
            list_cat = [i["name"] for i in data["tags"]][:17]
            self.data = {}
            return list_cat

        except requests.exceptions.Timeout as t:
            print("Request Timeout, please retry : ", t)
        except requests.exceptions.RequestException as err:
            print("Something went bad, please retry : :", err)

    def _fetch_products(self, page_size):
        """Request the products in respect for the categories loaded."""
        print(
            "Getting Products from API in respect to the"
            " Categories previously got"
        )
        fields = ",".join(keys)
        all_products = {}
        for category in self.list_cat:
            config = {
                "action": "process",
                # Get the result by category
                "tagtype_0": "categories",
                # the tag represents the article search
                "tag_0": category,
                "fields": fields,
                "tag_contains_0": "contains",
                # Number of articles per page
                # Min content 20, Max content 1000
                "page_size": page_size,
                # The API response in JSON
                "json": 1,
            }
            response = self._req(self.search_url, param=config)
            all_products[category] = response.json()
        return all_products

    def _req(self, url, param=None):
        """Small request function used multiple times."""
        response = requests.get(url, param)
        return response


class Cleaner:
    """This class will handle the data formatting before db use."""

    def __init__(self, data):
        """Initialize variables and launch filter_products."""
        self.data = data
        self.keys = keys
        self.list_cat = [categories for categories in self.data]
        self._dict_data = {}
        self.list_of_dictio = []
        self.barcode_list = []
        self.name_list = []

    def filter_product(self):
        """Get the data from json files and run checks."""
        for category in self.list_cat:
            for element in self.data[category]["products"]:
                if self._data_exist(element):
                    self.list_of_dictio.append(element)
            self._dict_data[category] = self.list_of_dictio
            self.list_of_dictio = []
        return self._dict_data

    def _data_exist(self, element):
        """Run trough the data, if something's missing it's discarded."""
        for x in self.keys:
            if (
                x not in element
                or element[x] == ""
                or len(element["id"]) != 13
            ):
                return False

        barcode = int(element["id"])
        if barcode in self.barcode_list:
            return False
        else:
            self.barcode_list.append(barcode)

        name = element["product_name_fr"].lower()
        if name in self.name_list:
            return False
        else:
            self.name_list.append(name)
        return True


def req_and_clean(page_size):
    """Main function to instantiate and launch operations."""
    r = RequestData()
    data = r.exec(page_size)
    c = Cleaner(data)
    data = c.filter_product()
    return data


if __name__ == "__main__":
    data = req_and_clean()
    print(data)

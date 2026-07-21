from data import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pages.urban_routes_page import UrbanRoutesPage

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls, name=None):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance":"ALL"})
        cls.driver = webdriver.Chrome(service=Service(), options=options)
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    #Direcciones
    def test_set_route(self):
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

    #Tarifa Comfort
    def test_comfort_tariff_selection(self):
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_icon()
        assert_text = self.routes_page.get_comfort_icon_assert().text

        assert assert_text == "Comfort"

    #Teléfono
    def test_fill_phone_number(self):
        self.routes_page.fill_phone_number(data.phone_number)

    #Tarjeta de Crédito
    def test_fill_card(self):
        card_number, card_code = data.card_number, data.card_code
        self.routes_page.add_credit_card(card_number, card_code)

        panel_text = self.routes_page.get_payment_method_panel_text()
        assert 'Tarjeta' in panel_text

        self.routes_page.close_payment_modal()

    #Mensaje para el conductor
    #def test_message_for_driver(self):
     #   message = data.message_for_driver
      #  self.routes_page.set_message_for_driver(message)
       # assert self.routes_page.get_message_for_driver() == message
        #assert message == 'Muéstrame el camino'
    def test_message_for_driver(self):
        expected_message = 'Muéstrame el camino'
        message = data.message_for_driver
        assert message == expected_message, f"El texto en data no coincide. Esperado: '{expected_message}', Obtenido: '{message}'"
        self.routes_page.set_message_for_driver(message)
        assert self.routes_page.get_message_for_driver() == expected_message

    # Manta y pañuelos
    def test_blanket_and_tissues(self):
        self.routes_page.click_blanket_and_tissues_switch()
        switch_element = self.driver.find_element(*self.routes_page.blanket_and_tissues_switch)
        assert switch_element.is_selected() or "checked" in switch_element.get_attribute("class")

    # Pedir 2 helados
    def test_ice_cream(self):
        self.routes_page.order_ice_cream(2)
        assert self.routes_page.get_ice_cream_count() == '2'

    #Pedir un taxi
    def test_order_taxi(self):
        self.routes_page.click_order_taxi_button()
        assert self.routes_page.get_search_modal().is_displayed()

   #Información del conductor
    def test_driver_info_appears(self):
        assert self.routes_page.get_driver_info().is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

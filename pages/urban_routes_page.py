from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from helpers.retrive_code import retrieve_phone_code

class UrbanRoutesPage:
#Direcciones
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

#Tarifa Comfort
    request_taxi_button = (By.CSS_SELECTOR, '.button.round')
    comfort_icon = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')
    comfort_icon_assert = (By.CSS_SELECTOR, '.tariff-cards .tcard.active .tcard-title')

#Teléfono
    phone_field_open = (By.CLASS_NAME, 'np-button')
    phone_field = (By.ID, 'phone')
    phone_confirm_button = (By.CSS_SELECTOR, 'button.button.full')

    sms_code_field = (By.ID, 'code')
    sms_confirm_button = (By.XPATH, '//button[normalize-space()="Confirmar"]')

#Tarjeta de crédito
    payment_method_button = (By.CLASS_NAME, 'pp-button')
    add_card_button = (By.CLASS_NAME, 'pp-plus')
    card_number_field = (By.ID, 'number')
    card_code_field = (By.CSS_SELECTOR, 'input#code.card-input')
    link_button = (By.XPATH, "//button[text()='Agregar']")
    close_payment_modal_button = (By.CSS_SELECTOR, '.payment-picker.open .section.active .close-button')
    payment_method_panel = (By.CLASS_NAME, 'payment-picker')

#Mensaje conductor
    message_field = (By.ID, 'comment')


# Requisitos del pedido
    requirements_header = (By.CLASS_NAME, "reqs-header")

# Manta y pañuelos
    blanket_and_tissues_switch = (
        By.XPATH,
        "//div[contains(@class,'r-sw-container')]//input[@class='switch-input']"
    )

# Helado
    ice_cream_plus_button = (
        By.XPATH,
        "//div[text()='Helado']/following-sibling::div//div[contains(@class,'counter-plus')]"
    )

    ice_cream_count_value = (
        By.XPATH,
        "//div[text()='Helado']/following-sibling::div//div[@class='counter-value']"
    )

#Pedir taxi
    order_taxi_button = (By.CSS_SELECTOR, 'button.smart-button')
    search_modal = (By.CLASS_NAME, 'order-header-title')
    driver_info = (By.CLASS_NAME, 'order-driver')

#Información del conductor
    driver_info = (By.CLASS_NAME, 'order-body')


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

#Configurar la dirección
    def set_from(self, from_address):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

#Tarifa Comfort
    def get_request_taxi_button(self):
        return self.wait.until(
            expected_conditions.element_to_be_clickable(self.request_taxi_button)
        )
    def click_request_taxi_button(self):
        self.get_request_taxi_button().click()

    def get_comfort_icon(self):
        return self.wait.until(
            expected_conditions.element_to_be_clickable(self.comfort_icon)
        )

    def click_comfort_icon(self):
        self.get_comfort_icon().click()

    def get_comfort_icon_assert(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(self.comfort_icon_assert)
        )

#Teléfono
    def click_phone_field_open(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.phone_field_open)
        ).click()

    def set_phone_number(self, phone_number):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.phone_field)
        ).send_keys(phone_number)

    def click_phone_confirm_button(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.phone_confirm_button)
        ).click()

    def get_sms_code_field(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(self.sms_code_field)
        )

    def set_sms_code(self, code):
        self.get_sms_code_field().send_keys(code)

    def click_sms_confirm_button(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.sms_confirm_button)
        ).click()

    def confirm_sms_code(self):
        code = retrieve_phone_code(self.driver)
        self.set_sms_code(code)
        self.click_sms_confirm_button()

    def fill_phone_number(self, phone_number):
        self.click_phone_field_open()
        self.set_phone_number(phone_number)
        self.click_phone_confirm_button()
        self.confirm_sms_code()

#Tarjeta de crédito
    def click_payment_method_button(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.payment_method_button)
        ).click()

    def click_add_card_button(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.add_card_button)
        ).click()

    def set_card_number(self, card_number):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.card_number_field)
        ).send_keys(card_number)

    def set_card_code(self, card_code):
        code_field = self.wait.until(
            expected_conditions.visibility_of_element_located(self.card_code_field)
        )
        code_field.send_keys(card_code)
        # El botón 'Link' no se activa hasta que el campo CVV pierda el foco.
        # Simulamos que la persona usuaria presiona TAB para quitar el foco.
        code_field.send_keys(Keys.TAB)

    def click_link_button(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.link_button)
        ).click()

    def add_credit_card(self, card_number, card_code):
        self.click_payment_method_button()
        self.click_add_card_button()
        self.set_card_number(card_number)
        self.set_card_code(card_code)
        self.click_link_button()

    def get_payment_method_panel_text(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(self.payment_method_panel)
        ).text

    def close_payment_modal(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.close_payment_modal_button)
        ).click()

#Mensaje para el conductor
    def set_message_for_driver(self, message):
        self.wait.until(
            expected_conditions.visibility_of_element_located(self.message_field)
        ).send_keys(message)

    def get_message_for_driver(self):
        return self.driver.find_element(*self.message_field).get_property('value')

#Requisitos del pedido
    def click_requirements_header(self):
        header = self.wait.until(
            expected_conditions.element_to_be_clickable(self.requirements_header)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", header)
        header.click()
        self.wait.until(
            expected_conditions.visibility_of_element_located(
                (By.CLASS_NAME, "reqs-body")
            )
        )

# Manta y pañuelos
    def click_blanket_and_tissues_switch(self):
        switch = self.wait.until(
            expected_conditions.presence_of_element_located(
                self.blanket_and_tissues_switch
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            switch
        )
        self.driver.execute_script(
            "arguments[0].click();",
            switch
        )

    def is_blanket_and_tissues_enabled(self):
        switch = self.wait.until(
            expected_conditions.presence_of_element_located(
                self.blanket_and_tissues_switch
            )
        )
        return switch.is_selected() or self.driver.find_element(
            By.XPATH, "//div[contains(@class,'r-sw-container')]//input[@class='switch-input']"
        ).get_attribute('checked')

# Helados
    def click_ice_cream_plus_button(self):
        plus = self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.ice_cream_plus_button
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            plus
        )

        self.driver.execute_script(
            "arguments[0].click();",
            plus
        )

    def order_ice_cream(self, quantity=2):
        for _ in range(quantity):
            self.click_ice_cream_plus_button()

    def get_ice_cream_count(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(
                self.ice_cream_count_value
            )
        ).text

#Pedir el taxi
    def click_order_taxi_button(self):
        self.wait.until(
            expected_conditions.element_to_be_clickable(self.order_taxi_button)
        ).click()

    def get_search_modal(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(self.search_modal)
        )

#Información del conductor
    def get_driver_info(self, timeout=60):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.visibility_of_element_located(self.driver_info)
        )
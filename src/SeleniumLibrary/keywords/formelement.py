# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.errors import ElementNotFound
from SeleniumLibrary.utils import is_noney


class FormElementKeywords(LibraryComponent):

    @keyword
    def submit_form(self, locator=None):
        """Submits a form identified by `locator`.

        If `locator` is empty, first form in the page will be submitted.
        Key attributes for forms are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self.info("Submitting form '%s'." % locator)
        if is_noney(locator):
            locator = 'tag:form'
        element = self.find_element(locator, tag='form')
        element.submit()

    @keyword
    def checkbox_should_be_selected(self, locator):
        """Verifies checkbox identified by `locator` is selected/checked.

        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self.info("Verifying checkbox '%s' is selected." % locator)
        element = self._get_checkbox(locator)
        if not element.is_selected():
            raise AssertionError("Checkbox '%s' should have been selected "
                                 "but was not." % locator)

    @keyword
    def checkbox_should_not_be_selected(self, locator):
        """Verifies checkbox identified by `locator` is not selected/checked.

        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self.info("Verifying checkbox '%s' is not selected." % locator)
        element = self._get_checkbox(locator)
        if element.is_selected():
            raise AssertionError("Checkbox '%s' should not have been "
                                 "selected." % locator)

    @keyword
    def page_should_contain_checkbox(self, locator, message=None, loglevel='INFO'):
        """Verifies checkbox identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self.assert_page_contains(locator, 'checkbox', message, loglevel)

    @keyword
    def page_should_not_contain_checkbox(self, locator, message=None, loglevel='INFO'):
        """Verifies checkbox identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self.assert_page_not_contains(locator, 'checkbox', message, loglevel)

    @keyword
    def select_checkbox(self, locator):
        """Selects checkbox identified by `locator`.

        Does nothing if checkbox is already selected. Key attributes for
        checkboxes are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        self.info("Selecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if not element.is_selected():
            element.click()

    @keyword
    def unselect_checkbox(self, locator):
        """Removes selection of checkbox identified by `locator`.

        Does nothing if the checkbox is not checked. Key attributes for
        checkboxes are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        self.info("Unselecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if element.is_selected():
            element.click()

    @keyword
    def page_should_contain_radio_button(self, locator, message=None, loglevel='INFO'):
        """Verifies radio button identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for radio buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self.assert_page_contains(locator, 'radio button', message, loglevel)

    @keyword
    def page_should_not_contain_radio_button(self, locator, message=None, loglevel='INFO'):
        """Verifies radio button identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for radio buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self.assert_page_not_contains(locator, 'radio button', message,
                                      loglevel)

    @keyword
    def radio_button_should_be_set_to(self, group_name, value):
        """Verifies radio button group identified by `group_name` has its selection set to `value`.

        See `Select Radio Button` for information about how radio buttons are
        located.
        """
        self.info("Verifying radio button '%s' has selection '%s'."
                  % (group_name, value))
        elements = self._get_radio_buttons(group_name)
        actual_value = self._get_value_from_radio_buttons(elements)
        if actual_value is None or actual_value != value:
            raise AssertionError("Selection of radio button '%s' should have "
                                 "been '%s' but was '%s'."
                                 % (group_name, value, actual_value))

    @keyword
    def radio_button_should_not_be_selected(self, group_name):
        """Verifies radio button group identified by `group_name` has no selection.

        See `Select Radio Button` for information about how radio buttons are
        located.
        """
        self.info("Verifying radio button '%s' has no selection." % group_name)
        elements = self._get_radio_buttons(group_name)
        actual_value = self._get_value_from_radio_buttons(elements)
        if actual_value is not None:
            raise AssertionError("Radio button group '%s' should not have "
                                 "had selection, but '%s' was selected."
                                 % (group_name, actual_value))

    @keyword
    def select_radio_button(self, group_name, value):
        """Sets selection of radio button group identified by `group_name` to `value`.

        The radio button to be selected is located by two arguments:
        - `group_name` is used as the name of the radio input
        - `value` is used for the value attribute or for the id attribute

        The XPath used to locate the correct radio button then looks like this:
        //input[@type='radio' and @name='group_name' and (@value='value' or @id='value')]

        Examples:
        | Select Radio Button | size | XL | # Matches HTML like <input type="radio" name="size" value="XL">XL</input> |
        | Select Radio Button | size | sizeXL | # Matches HTML like <input type="radio" name="size" value="XL" id="sizeXL">XL</input> |
        """
        self.info("Selecting '%s' from radio button '%s'."
                  % (value, group_name))
        element = self._get_radio_button_with_value(group_name, value)
        if not element.is_selected():
            element.click()

    @keyword
    def choose_file(self, locator, file_path):
        """Inputs the `file_path` into file input field found by `locator`.

        This keyword is most often used to input files into upload forms.
        The file specified with `file_path` must be available on the same host
        where the Selenium Server is running.

        Example:
        | Choose File | my_upload_field | /home/user/files/trades.csv |
        """
        if not os.path.isfile(file_path):
            raise ValueError("File '%s' does not exist on the local file "
                             "system." % file_path)
        self.find_element(locator).send_keys(file_path)

    @keyword
    def input_password(self, locator, text):
        """Types the given password into text field identified by `locator`.

        Difference between this keyword and `Input Text` is that this keyword
        does not log the given password. See `introduction` for details about
        locating elements.
        """
        self.info("Typing password into text field '%s'." % locator)
        self._input_text_into_text_field(locator, text)

    @keyword
    def input_text(self, locator, text):
        """Types the given `text` into text field identified by `locator`.

        See `introduction` for details about locating elements.
        """
        self.info("Typing text '%s' into text field '%s'." % (text, locator))
        self._input_text_into_text_field(locator, text)

    @keyword
    def page_should_contain_textfield(self, locator, message=None, loglevel='INFO'):
        """Verifies text field identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self.assert_page_contains(locator, 'text field', message, loglevel)

    @keyword
    def page_should_not_contain_textfield(self, locator, message=None, loglevel='INFO'):
        """Verifies text field identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self.assert_page_not_contains(locator, 'text field', message, loglevel)

    @keyword
    def textfield_should_contain(self, locator, expected, message=None):
        """Verifies text field identified by `locator` contains text `expected`.

        `message` can be used to override default error message.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        actual = self._get_value(locator, 'text field')
        if expected not in actual:
            if is_noney(message):
                message = "Text field '%s' should have contained text '%s' "\
                          "but it contained '%s'." % (locator, expected, actual)
            raise AssertionError(message)
        self.info("Text field '%s' contains text '%s'." % (locator, expected))

    @keyword
    def textfield_value_should_be(self, locator, expected, message=None):
        """Verifies the value in text field identified by `locator` is exactly `expected`.

        `message` can be used to override default error message.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        actual = self._get_value(locator, 'text field')
        if actual != expected:
            if is_noney(message):
                message = "Value of text field '%s' should have been '%s' "\
                          "but was '%s'." % (locator, expected, actual)
            raise AssertionError(message)
        self.info("Content of text field '%s' is '%s'." % (locator, expected))

    @keyword
    def textarea_should_contain(self, locator, expected, message=None):
        """Verifies text area identified by `locator` contains text `expected`.

        `message` can be used to override default error message.

        Key attributes for text areas are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        actual = self._get_value(locator, 'text area')
        if expected not in actual:
            if is_noney(message):
                message = "Text area '%s' should have contained text '%s' " \
                          "but it had '%s'." % (locator, expected, actual)
            raise AssertionError(message)
        self.info("Text area '%s' contains text '%s'." % (locator, expected))

    @keyword
    def textarea_value_should_be(self, locator, expected, message=None):
        """Verifies the value in text area identified by `locator` is exactly `expected`.

        `message` can be used to override default error message.

        Key attributes for text areas are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        actual = self._get_value(locator, 'text area')
        if expected != actual:
            if is_noney(message):
                message = "Text area '%s' should have had text '%s' " \
                          "but it had '%s'." % (locator, expected, actual)
            raise AssertionError(message)
        self.info("Content of text area '%s' is '%s'." % (locator, expected))

    @keyword
    def click_button(self, locator):
        """Clicks a button identified by `locator`.

        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self.info("Clicking button '%s'." % locator)
        element = self.find_element(locator, tag='input', required=False)
        if not element:
            element = self.find_element(locator, tag='button')
        element.click()

    @keyword
    def page_should_contain_button(self, locator, message=None, loglevel='INFO'):
        """Verifies button identified by `locator` is found from current page.

        This keyword searches for buttons created with either `input` or `button` tag.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        try:
            self.assert_page_contains(locator, 'input', message, loglevel)
        except AssertionError:
            self.assert_page_contains(locator, 'button', message, loglevel)

    @keyword
    def page_should_not_contain_button(self, locator, message=None, loglevel='INFO'):
        """Verifies button identified by `locator` is not found from current page.

        This keyword searches for buttons created with either `input` or `button` tag.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self.assert_page_not_contains(locator, 'button', message, loglevel)
        self.assert_page_not_contains(locator, 'input', message, loglevel)

    def _get_value(self, locator, tag):
        return self.find_element(locator, tag).get_attribute('value')

    def _get_checkbox(self, locator):
        return self.find_element(locator, tag='input')

    def _get_radio_buttons(self, group_name):
        xpath = "xpath://input[@type='radio' and @name='%s']" % group_name
        self.debug('Radio group locator: ' + xpath)
        elements = self.find_elements(xpath)
        if not elements:
            raise ElementNotFound("No radio button with name '%s' found."
                                  % group_name)
        return elements

    def _get_radio_button_with_value(self, group_name, value):
        xpath = "xpath://input[@type='radio' and @name='%s' and " \
                "(@value='%s' or @id='%s')]" % (group_name, value, value)
        self.debug('Radio group locator: ' + xpath)
        try:
            return self.find_element(xpath)
        except ElementNotFound:
            raise ElementNotFound("No radio button with name '%s' and "
                                  "value '%s' found." % (group_name, value))

    def _get_value_from_radio_buttons(self, elements):
        for element in elements:
            if element.is_selected():
                return element.get_attribute('value')
        return None

    def _input_text_into_text_field(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

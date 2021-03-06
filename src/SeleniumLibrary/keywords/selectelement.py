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

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.utils import is_truthy


class SelectElementKeywords(LibraryComponent):

    @keyword
    def get_list_items(self, locator, value=False):
        """Returns the labels or values in the select list identified by `locator`.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.

        Example:
        | ${labels1} = | Get List Items | xpath=//h1 |
        | ${labels2} = | Get List Items | xpath=//h1 | value=${False} |
        | ${values} = | Get List Items | xpath=//h1 | value=True |
        | Should Be Equal | ${labels1} | ${labels2} |
        """
        select, options = self._get_select_list_options(locator)
        if is_truthy(value):
            return self._get_values_for_options(options)
        else:
            return self._get_labels_for_options(options)

    @keyword
    def get_selected_list_label(self, locator):
        """Returns the visible label of the selected element from the select list identified by `locator`.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        select = self._get_select_list(locator)
        return select.first_selected_option.text

    @keyword
    def get_selected_list_labels(self, locator):
        """Returns the visible labels of selected elements (as a list) from the select list identified by `locator`.

        Fails if there is no selection.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        select, options = self._get_select_list_options_selected(locator)
        if not options:
            raise ValueError("List '%s' does not have any selected values."
                             % locator)
        return self._get_labels_for_options(options)

    @keyword
    def get_selected_list_value(self, locator):
        """Returns the value of the selected element from the select list identified by `locator`.

        Return value is read from `value` attribute of the selected element.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        select = self._get_select_list(locator)
        return select.first_selected_option.get_attribute('value')

    @keyword
    def get_selected_list_values(self, locator):
        """Returns the values of selected elements (as a list) from the select list identified by `locator`.

        Fails if there is no selection.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        select, options = self._get_select_list_options_selected(locator)
        # TODO: Should return an empty list, not fail
        if not options:
            raise ValueError("Select list with locator '%s' does not have any selected values")
        return self._get_values_for_options(options)

    @keyword
    def list_selection_should_be(self, locator, *items):
        """Verifies the selection of select list identified by `locator` is exactly `*items`.

        If you want to test that no option is selected, simply give no `items`.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        items_str = items and "option(s) [ %s ]" % " | ".join(items) or "no options"
        self.info("Verifying list '%s' has %s selected." % (locator, items_str))
        items = list(items)
        self.page_should_contain_list(locator)
        select, options = self._get_select_list_options_selected(locator)
        if not items and len(options) == 0:
            return
        selected_values = self._get_values_for_options(options)
        selected_labels = self._get_labels_for_options(options)
        err = "List '%s' should have had selection [ %s ] but it was [ %s ]" \
            % (locator, ' | '.join(items), ' | '.join(selected_labels))
        for item in items:
            if item not in selected_values + selected_labels:
                raise AssertionError(err)
        for selected_value, selected_label in zip(selected_values, selected_labels):
            if selected_value not in items and selected_label not in items:
                raise AssertionError(err)

    @keyword
    def list_should_have_no_selections(self, locator):
        """Verifies select list identified by `locator` has no selections.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        self.info("Verifying list '%s' has no selection." % locator)
        select, options = self._get_select_list_options_selected(locator)
        if options:
            selected_labels = self._get_labels_for_options(options)
            items_str = " | ".join(selected_labels)
            raise AssertionError("List '%s' should have had no selection "
                                 "(selection was [ %s ])" % (locator, items_str))

    @keyword
    def page_should_contain_list(self, locator, message=None, loglevel='INFO'):
        """Verifies select list identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for lists are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self.assert_page_contains(locator, 'list', message, loglevel)

    @keyword
    def page_should_not_contain_list(self, locator, message=None, loglevel='INFO'):
        """Verifies select list identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for lists are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self.assert_page_not_contains(locator, 'list', message, loglevel)

    @keyword
    def select_all_from_list(self, locator):
        """Selects all values from multi-select list identified by `id`.

        Key attributes for lists are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self.info("Selecting all options from list '%s'." % locator)

        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Keyword 'Select all from list' works only for "
                               "multiselect lists.")

        for i in range(len(select.options)):
            select.select_by_index(i)

    @keyword
    def select_from_list(self, locator, *items):
        """Selects `*items` from list identified by `locator`

        If more than one value is given for a single-selection list, the last
        value will be selected. If the target list is a multi-selection list,
        and `*items` is an empty list, all values of the list will be selected.

        *items try to select by value then by label.

        It's faster to use 'by index/value/label' functions.

        An exception is raised for a single-selection list if the last
        value does not exist in the list and a warning for all other non-
        existing items. For a multi-selection list, an exception is raised
        for any and all non-existing values.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        non_existing_items = []

        items_str = items and "option(s) '%s'" % ", ".join(items) or "all options"
        self.info("Selecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)

        if not items:
            for i in range(len(select.options)):
                select.select_by_index(i)
            return

        for item in items:
            try:
                select.select_by_value(item)
            except:
                try:
                    select.select_by_visible_text(item)
                except:
                    non_existing_items = non_existing_items + [item]
                    continue

        if any(non_existing_items):
            if select.is_multiple:
                raise ValueError("Options '%s' not in list '%s'." % (", ".join(non_existing_items), locator))
            else:
                if any (non_existing_items[:-1]):
                    items_str = non_existing_items[:-1] and "Option(s) '%s'" % ", ".join(non_existing_items[:-1])
                    self.warn("%s not found within list '%s'." % (items_str, locator))
                if items and items[-1] in non_existing_items:
                    raise ValueError("Option '%s' not in list '%s'." % (items[-1], locator))

    @keyword
    def select_from_list_by_index(self, locator, *indexes):
        """Selects `*indexes` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not indexes:
            raise ValueError("No index given.")
        items_str = "index(es) '%s'" % ", ".join(indexes)
        self.info("Selecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        for index in indexes:
            select.select_by_index(int(index))

    @keyword
    def select_from_list_by_value(self, locator, *values):
        """Selects `*values` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not values:
            raise ValueError("No value given.")
        items_str = "value(s) '%s'" % ", ".join(values)
        self.info("Selecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        for value in values:
            select.select_by_value(value)

    @keyword
    def select_from_list_by_label(self, locator, *labels):
        """Selects `*labels` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not labels:
            raise ValueError("No value given.")
        items_str = "label(s) '%s'" % ", ".join(labels)
        self.info("Selecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        for label in labels:
            select.select_by_visible_text(label)

    @keyword
    def unselect_from_list(self, locator, *items):
        """Unselects given values from select list identified by locator.

        As a special case, giving empty list as `*items` will remove all
        selections.

        *items try to unselect by value AND by label.

        It's faster to use 'by index/value/label' functions.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        items_str = items and "option(s) '%s'" % ", ".join(items) or "all options"
        self.info("Unselecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Keyword 'Unselect from list' works only for multiselect lists.")

        if not items:
            select.deselect_all()
            return

        select, options = self._get_select_list_options(select)
        for item in items:
            # Only Selenium 2.52 and newer raise exceptions when there is no match.
            # For backwards compatibility reasons we want to ignore them.
            try:
                select.deselect_by_value(item)
            except NoSuchElementException:
                pass
            try:
                select.deselect_by_visible_text(item)
            except NoSuchElementException:
                pass

    @keyword
    def unselect_from_list_by_index(self, locator, *indexes):
        """Unselects `*indexes` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not indexes:
            raise ValueError("No index given.")

        items_str = "index(es) '%s'" % ", ".join(indexes)
        self.info("Unselecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Keyword 'Unselect from list' works only for multiselect lists.")

        for index in indexes:
            select.deselect_by_index(int(index))

    @keyword
    def unselect_from_list_by_value(self, locator, *values):
        """Unselects `*values` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not values:
            raise ValueError("No value given.")
        items_str = "value(s) '%s'" % ", ".join(values)
        self.info("Unselecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Keyword 'Unselect from list' works only for multiselect lists.")

        for value in values:
            select.deselect_by_value(value)

    @keyword
    def unselect_from_list_by_label(self, locator, *labels):
        """Unselects `*labels` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not labels:
            raise ValueError("No value given.")
        items_str = "label(s) '%s'" % ", ".join(labels)
        self.info("Unselecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Keyword 'Unselect from list' works only for multiselect lists.")

        for label in labels:
            select.deselect_by_visible_text(label)

    def _get_labels_for_options(self, options):
        labels = []
        for option in options:
            labels.append(option.text)
        return labels

    def _get_select_list(self, locator):
        el = self.find_element(locator, tag='select')
        return Select(el)

    def _get_select_list_options(self, select_list_or_locator):
        if isinstance(select_list_or_locator, Select):
            select = select_list_or_locator
        else:
            select = self._get_select_list(select_list_or_locator)
        return select, select.options

    def _get_select_list_options_selected(self, locator):
        select = self._get_select_list(locator)
        # TODO: Handle possible exception thrown by all_selected_options
        return select, select.all_selected_options

    def _get_values_for_options(self, options):
        values = []
        for option in options:
            values.append(option.get_attribute('value'))
        return values

    def _is_multiselect_list(self, select):
        multiple_value = select.get_attribute('multiple')
        if multiple_value is not None and (multiple_value == 'true' or multiple_value == 'multiple'):
            return True
        return False

    def _unselect_all_options_from_multi_select_list(self, select):
        self.browser.execute_script("arguments[0].selectedIndex = -1;", select)

    def _unselect_option_from_multi_select_list(self, select, options, index):
        if options[index].is_selected():
            options[index].click()

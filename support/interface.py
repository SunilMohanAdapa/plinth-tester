#
# This file is part of Plinth-tester.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

sys_modules = [
    'config', 'users', 'networks', 'names', 'letsencrypt', 'upgrades',
    'diagnostics', 'firewall', 'datetime', 'avahi', 'monkeysphere', 'power'
]


def login(browser, url, username, password):
    browser.visit(url)
    if browser.find_by_id('logout-nojs'):
        return  # already logged in

    browser.find_link_by_href('/plinth/accounts/login/').first.click()
    login = browser.find_by_value('Login')
    if login:
        browser.fill('username', username)
        browser.fill('password', password)
        login.click()
    else:
        browser.find_link_by_href('/plinth/firstboot/state1/').first.click()
        browser.fill('username', username)
        browser.find_by_id('id_password1').fill(password)
        browser.find_by_id('id_password2').fill(password)
        browser.find_by_value('Box it up!').click()


def is_login_prompt(browser):
    return all([
        browser.find_by_id('id_username'),
        browser.find_by_id('id_password')])


def nav_to_module(browser, module):
    browser.find_link_by_href('/plinth/').first.click()
    if module in sys_modules:
        browser.find_link_by_href('/plinth/sys/').first.click()
        browser.find_link_by_href('/plinth/sys/' + module + '/').first.click()
    else:
        browser.find_link_by_href('/plinth/apps/').first.click()
        browser.find_link_by_href('/plinth/apps/' + module + '/').first.click()


def submit(browser):
    browser.find_by_value('Submit').click()


def create_user(browser, name, password):
    nav_to_module(browser, 'users')
    browser.find_link_by_href('/plinth/sys/users/create/').first.click()
    browser.find_by_id('id_username').fill(name)
    browser.find_by_id('id_password1').fill(password)
    browser.find_by_id('id_password2').fill(password)
    browser.find_by_value('Create User').click()


def rename_user(browser, old_name, new_name):
    nav_to_module(browser, 'users')
    browser.find_link_by_href('/plinth/sys/users/' + old_name +
                              '/edit/').first.click()
    browser.find_by_id('id_username').fill(new_name)
    browser.find_by_value('Save Changes').click()


def delete_user(browser, name):
    nav_to_module(browser, 'users')
    browser.find_link_by_href('/plinth/sys/users/' + name +
                              '/delete/').first.click()
    browser.find_by_value('Delete ' + name).click()


def is_user(browser, name):
    nav_to_module(browser, 'users')
    return browser.is_text_present(name)

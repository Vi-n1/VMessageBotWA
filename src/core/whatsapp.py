# -*- coding: utf-8 -*-
from ._core import WhatsAppCore
from .exceptions import UnsupportedBrowserException
from os import path, getlogin


class WhatsApp(WhatsAppCore):
    """
    Interaction with WhatsApp.
    """

    def __init__(self):
        super().__init__()
        self.__USER = getlogin()

    @property
    def browser(self) -> str:
        """The name of the browser used to access WhatsApp Web.

        Returns:
            str: The name of the browser, such as 'chrome', 'edge', or 'firefox'.
        """
        return self._get_browser()

    @browser.setter
    def browser(self, browser: str):
        """Set the browser to use for accessing WhatsApp Web.

        Args:
            browser (str): The name of the browser, such as 'chrome', 'edge', or 'firefox'.

        Raises:
            UnsupportedBrowserException: If the browser is not supported.
        """
        browser = browser.lower()
        match browser:

            # Create the browser instance as chosen.
            case 'chrome':
                from selenium.webdriver import (
                    Chrome,
                    ChromeService,
                    ChromeOptions,
                )

                service = ChromeService()
                options = ChromeOptions()
                user_data_dir = self.__get_user_data_dir_chrome()
                options.add_argument(f'--user-data-dir={user_data_dir}')
                self._set_browser(Chrome(options, service))

            case 'edge':
                from selenium.webdriver import Edge, EdgeService, EdgeOptions

                service = EdgeService()
                options = EdgeOptions()
                user_data_dir = self.__get_user_data_dir_edge()
                options.add_argument(f'--user-data-dir={user_data_dir}')
                self._set_browser(Edge(options, service))

            case 'firefox':
                from selenium.webdriver import (
                    Firefox,
                    FirefoxService,
                    FirefoxOptions,
                )

                service = FirefoxService()
                options = FirefoxOptions()
                user_data_dir = self.__get_user_data_dir_firefox()
                options.add_argument(f'--user-data-dir={user_data_dir}')
                self._set_browser(Firefox(options, service))

            case _:
                # If the chosen browser is not one of the previous options, an exception is raised.
                raise UnsupportedBrowserException()

    def send_audio(self, receiver: str, audio_path: str):
        """Send an audio to a receiver.

        Args:
            receiver (str): The phone number or the group code of the receiver.
            audio_path (str): The path of the audio file to be sent.
        """
        self._send_audio(receiver, audio_path)

    def send_image(self, receiver: str, img_path: str, message: str = None):
        """Send an image to a receiver with or without text.

        Args:
            receiver (str): The phone number or the group code of the receiver.
            path_img (str): The path of the image file to be sent.
            message (str, optional): The text message to be sent along with the image. Defaults to None.
        """
        self._send_image(receiver, img_path, message)

    def send_text(self, receiver: str, message: str):
        """Send a text message to a receiver.

        Args:
            receiver (str): The phone number or the group code of the receiver.
            message (str): The text message to be sent.
        """
        self._send_text(receiver, message)

    def set_wait(self, seconds: float):
        """Set the implicit wait time for the browser.

        Args:
            seconds (float): The number of seconds to wait for an element to be found.

        Raises:
            ValueError: If the seconds argument is not a float or an int.
            AttributeError: If the browser object is not instantiated.
        """
        if isinstance(seconds, float | int):
            try:
                self._set_timeout(seconds)
            except AttributeError:
                raise AttributeError('Uninstantiated browser object')
        else:
            raise ValueError(
                f'An int or float is expected and not {type(seconds)}'
            )

    def __get_user_data_dir_chrome(self) -> str:
        """Get the user data directory for Chrome browser.

        Returns:
            str: The path of the user data directory, or an empty string if not found.
        """
        normal_path = f'C:\\Users\\{self.__USER}\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
        downloaded_path = f'C:\\Users\\{self.__USER}\\AppData\\Local\\Google\\Chrome for Testing\\User Data\\Default'
        roaming_path = '%APPDATA%\\Google\\Chrome\\User Data\\Default'
        roaming_onedrive_path = (
            '%ONEDRIVE%\\Google\\Chrome\\User Data\\Default'
        )
        if path.isdir(normal_path):
            return normal_path

        if path.isdir(downloaded_path):
            return downloaded_path

        elif path.isdir(roaming_path):
            return roaming_path

        elif path.isdir(roaming_onedrive_path):
            return roaming_onedrive_path

        return ''

    def __get_user_data_dir_edge(self) -> str:
        """Get the user data directory for Edge browser.

        Returns:
            str: The path of the user data directory, or an empty string if not found.
        """
        normal_path = f'C:\\Users\\{self.__USER}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default'
        roaming_path = '%APPDATA%\\Microsoft\\Edge\\User Data\\Default'
        roaming_onedrive_path = (
            '%ONEDRIVE%\\Microsoft\\Edge\\User Data\\Default'
        )
        if path.isdir(normal_path):
            return normal_path

        elif path.isdir(roaming_path):
            return roaming_path

        elif path.isdir(roaming_onedrive_path):
            return roaming_onedrive_path

        return ''

    def __get_user_data_dir_firefox(self) -> str:
        """Get the user data directory for Firefox browser.

        Returns:
            str: The path of the user data directory, or an empty string if not found.
        """
        normal_path = f'C:\\Users\\{self.__USER}\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\'
        roaming_path = '%APPDATA%\\Mozilla\\Firefox\\Profiles\\'
        roaming_onedrive_path = '%ONEDRIVE%\\Microsoft\\Edge\\User Data\\'
        if path.isdir(normal_path):
            return normal_path

        elif path.isdir(roaming_path):
            return roaming_path

        elif path.isdir(roaming_onedrive_path):
            return roaming_onedrive_path

        return ''

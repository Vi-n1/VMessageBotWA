# -*- coding: utf-8 -*-
from .exceptions import (
    FailedLoginException,
    ElementNotFoundException,
    InvalidFileException,
)

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Edge, Chrome, Firefox

from time import sleep


class WhatsAppCore:
    """
    WhatsApp core implements all intentions with WhatsApp web
    """

    def __init__(self):
        self.__link = 'https://web.whatsapp.com/{}'
        self.__SECONDS_TO_NEXT_STEP = 1
        self.__msg: str
        self.__browser: Edge | Chrome | Firefox
        self.__file_path: str

    def _get_browser(self) -> str:
        """Returns the name of the current browser

        Returns:
            str: Name of the browser
        """
        return self.__browser.name

    def _set_browser(self, browser: Edge | Chrome | Firefox) -> None:
        if isinstance(browser, (Edge, Chrome, Firefox)):
            self.__browser = browser

    def _set_timeout(self, seconds: float | int) -> None:
        self.__browser.implicitly_wait(seconds)

    def _send_audio(self, receiver: str, audio_path: str) -> None:
        if self.__receiver_is_valid(receiver):
            if self.__file_path_is_valid(audio_path):
                self.__file_path = audio_path
                self.__set_link(receiver)
                self.__open_browser()
                self.__open_menu_attach()
                self.__attach_document()
                self.__paste_file_path()
                self.__submit_file()
                sleep(self.__SECONDS_TO_NEXT_STEP + 2)

            else:
                raise InvalidFileException()

    def _send_image(
        self, receiver: str, img_path: str, message: str = None
    ) -> None:
        if self.__receiver_is_valid(receiver):
            if self.__file_path_is_valid(img_path):
                self.__file_path = img_path
                self.__set_link(receiver)
                self.__open_browser()
                self.__open_menu_attach()
                self.__attach_video_or_img()
                self.__paste_file_path()
                if message:
                    self.__msg = message
                    self.__write_caption()

                self.__submit_file()
                sleep(self.__SECONDS_TO_NEXT_STEP + 2)

            else:
                raise InvalidFileException()

    def _send_text(self, receiver: str, message: str) -> None:
        """Send a text message to a receiver.

        Args:
            receiver (str): The phone number or the group code of the receiver.
            message (str): The text message to be sent.

        Raises:
            ValueError: If the receiver or the message are invalid.
            FailedLoginException: If the user is not logged in to WhatsApp Web.
        """
        if self.__receiver_is_valid(receiver):
            if message:
                self.__msg = message
                self.__set_link(receiver)
                self.__open_browser()
                self.__write_pure_text()
                self.__submit_text()
                sleep(self.__SECONDS_TO_NEXT_STEP + 2)
            else:
                raise ValueError(
                    f'{message} expects a string containing the message'
                )
        else:
            raise ValueError(
                f'{receiver} expects a string with numbers or group identifier'
            )

    def __attach_video_or_img(self) -> None:
        """Upload a video or image

        Raises:
            ElementNotFound: If the video or image element is not found after the timeout.
        """
        try:
            video_or_img_class = (
                'erpdyial.tviruh8d.gfz4du6o.r7fjleex.lhj4utae.le5p0ye3'
            )
            video_or_img = self.__browser.find_elements(
                By.CLASS_NAME, video_or_img_class
            )
            video_or_img[1].click()

        except TimeoutException:
            raise ElementNotFoundException()

    def __attach_document(self) -> None:
        """Upload a document

        Raises:
            ElementNotFoundException: _description_
        """
        try:
            document_class = (
                'erpdyial.tviruh8d.gfz4du6o.r7fjleex.lhj4utae.le5p0ye3'
            )
            document = self.__browser.find_elements(
                By.CLASS_NAME, document_class
            )
            document[0].click()

        except TimeoutException:
            raise ElementNotFoundException()

    def __file_path_is_valid(self, file_path) -> bool:
        from os.path import isfile

        return isfile(file_path)

    def __paste_file_path(self):
        """Paste the file path into the file dialog and press enter"""
        from pathlib import Path
        from keyboard import send, write

        path = str(Path(self.__file_path))
        sleep(self.__SECONDS_TO_NEXT_STEP)
        write(path)
        sleep(self.__SECONDS_TO_NEXT_STEP)
        send('enter')

    def __open_browser(self) -> None:
        """Open the WhatsApp Web link in the browser and login if needed.

        Raises:
            FailedLoginException: If the user is not logged in to WhatsApp Web.
        """
        self.__browser.get(self.__link)

        # Login screen title, used to identify whether you are on the login screen.
        no_login = self.__browser.find_elements(
            By.CLASS_NAME, 'landing-title._2K09Y'
        )

        if no_login:
            # 20 seconds to login.
            sleep(20)

            if no_login:
                # If the user does not log in, an exception is raised.
                raise FailedLoginException()

    def __open_menu_attach(self) -> None:
        """Open the menu to attach files or images.

        Raises:
            ElementNotFound: If the menu element is not found after the timeout.
        """
        try:
            menu_attach_class = 'bo8jc6qi.p4t1lx4y.brjalhku'
            menu_attach = self.__browser.find_elements(
                By.CLASS_NAME, menu_attach_class
            )
            menu_attach[0].click()

        except TimeoutException:
            raise ElementNotFoundException()

    def __receiver_is_valid(self, receiver) -> None:
        """Check if the receiver is a valid phone number or group code.

        Args:
            receiver (str): The phone number or the group code of the receiver.

        Returns:
            bool: True if the receiver is valid, False otherwise.
        """
        if isinstance(receiver, str) and (
            receiver.isalpha() or receiver.isalnum()
        ):
            return True
        return False

    def __set_link(self, receiver: str) -> None:
        """Set the WhatsApp Web link according to the type of receiver.

        Args:
            receiver (str): The phone number or the group code of the receiver.
        """
        if receiver.isnumeric():
            self.__link = self.__link.format(f'send?phone={receiver}')

        elif receiver.isalnum():
            self.__link = self.__link.format(f'accept?code={receiver}')

    def __submit_file(self) -> None:
        """Click the send button to submit the image."""

        # Send button class.
        button = (
            'p357zi0d.gndfcl4n.ac2vgrno.mh8l8k0y.'
            + 'k45dudtp.i5tg98hk.f9ovudaz.przvwfww.gx1rr48f.'
            + 'f8jlpxt4.hnx8ox4h.k17s6i4e.ofejerhi.os0tgls2.'
            + 'g9p5wyxn.i0tg5vk9.aoogvgrq.o2zu3hjb.hftcxtij.'
            + 'rtx6r8la.e3b81npk.oa9ii99z.p1ii4mzz'
        )
        button_send = self.__browser.find_elements(By.CLASS_NAME, button)
        button_send[0].click()

    def __submit_text(self) -> None:
        """Click the send button to submit the text."""

        # Send button class.
        button = 'tvf2evcx.oq44ahr5.lb5m6g5c.svlsagor.p2rjqpw5.epia9gcq'
        button_send = self.__browser.find_elements(By.CLASS_NAME, button)
        button_send[0].click()

    def __write_pure_text(self) -> None:
        """Write the text message."""

        # Text box class.
        text_box_pure = 'selectable-text.copyable-text.iq0m558w.g0rxnol2'
        text_box_pure_send = self.__browser.find_elements(
            By.CLASS_NAME, text_box_pure
        )
        text_box_pure_send[1].send_keys(self.__msg)

    def __write_caption(self):
        """Write the caption text."""

        # Text box class.
        text_box_caption = 'to2l77zo.gfz4du6o.ag5g9lrv.fe5nidar.kao4egtt'
        text_box_caption_send = self.__browser.find_elements(
            By.CLASS_NAME, text_box_caption
        )
        text_box_caption_send[0].send_keys(self.__msg)

from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDIconButton, MDFloatingActionButton, MDRectangleFlatButton
from kivy.core.text import LabelBase
from kivymd.uix.list import OneLineListItem
import pyrebase
import webbrowser
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from kivymd.uix.dialog import MDDialog
from kivyauth.utils import login_providers, auto_login
from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivyauth.utils import login_providers
from kivy import platform
from kivy.clock import Clock
import os
# from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import sys
import certifi
from kivy.uix.boxlayout import BoxLayout
from kivyauth.utils import stop_login
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.snackbar import Snackbar
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.slider import MDSlider
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar

import pygame
import os
Window.size = (300, 550)
class pop_up(MDDialog):
    tshow = ''

    def show(self):
        btn_close = MDFlatButton(text='close', on_release=self.dismis2)
        self.dilog = MDDialog(title='Incorrect', text=f'{self.tshow}',
                              size_hint=(0.7, 0.2),
                              buttons={btn_close})
        self.dilog.open()

    def dismis2(self, obj):
        self.dilog.dismiss()


class pop_up2(MDDialog):
    tshow = ''

    def show(self):
        btn_close = MDFlatButton(text='close', on_release=self.dismis2)
        self.dilog = MDDialog(title='Cryptocoin Team ', text=f'{self.tshow}',
                              size_hint=(0.7, 0.2),
                              buttons={btn_close})
        self.dilog.open()

    def dismis2(self, obj):
        self.dilog.dismiss()


class Welcome(Screen):
    pass
class LoginScreen(Screen):
    def Login_btn(self):
        btn = MDFlatButton(text="CANCEL")
        btn.bind(on_release=lambda *args: (self.dialog.dismiss()))
        self.dialog = MDDialog(
            title="",
            size_hint_x=None,
            size_hint_y=None,
            width="250dp",
            type="custom",
            auto_dismiss=False,
            # content_cls=Content(),
            buttons=[btn],
        )
        self.dialog.open()
        try:
            if len(self.password) < 8:
                self.dialog.dismiss()
                pop = pop_up()
                pop.tshow = 'Your Enter Password Is less Then 8 characters'
                pop.show()
                self.dialog.dismiss()

            else:
                
                
                self.manager.current = 'music'

        except:
            pop = pop_up()
            pop.tshow = 'you password and Email incorrect'
            pop.show()
            self.dialog.dismiss()
class Content(Screen):
    pass
class FirstScreen(Screen):
    pass
class CreateScreen(Screen):
    def create_acc(self):
        oper = True
        if len(self.username) == 0:
            oper = False
            pop = pop_up()
            pop.tshow = 'Username Field Is Empty'
            pop.show()
        else:
            if len(self.firstname) == 0:
                oper = False
                pop = pop_up()
                pop.tshow = 'First Name Field is Empty'
                pop.show()
            else:
                if len(self.lastname) == 0:
                    oper = False
                    pop = pop_up()
                    pop.tshow = 'Last Name Field  is Empty'
                    pop.show()
                else:
                    if len(self.password) == 0:
                        oper = False
                        pop = pop_up()
                        pop.tshow = 'Password Field is Empty'
                        pop.show()
                    else:
                        if len(self.password) < 8:
                            oper = False
                            pop = pop_up()
                            pop.tshow = 'Your Password Is 8 less then'
                            pop.show()
        if oper:
            btn = MDFlatButton(text="CANCEL")
            btn.bind(on_release=lambda *args: (self.dialog.dismiss()))
            self.dialog = MDDialog(
                title="",
                size_hint_x=None,
                size_hint_y=None,
                width="250dp",
                type="custom",
                auto_dismiss=False,
                content_cls=Content(),
                buttons=[btn],
            )
            self.dialog.open()
class MusicScreen(Screen):
   
    def next_track(self):
        # Implement logic to play the next track
        pass

    def previous_track(self):
        # Implement logic to play the previous track
        pass


sm = ScreenManager()
sm.add_widget(CreateScreen(name='create'))
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(FirstScreen(name='first'))
sm.add_widget(CreateScreen(name='create'))
sm.add_widget(Content(name='content'))
sm.add_widget(MusicScreen(name='Music'))


class DemoApp(MDApp):

    def build(self):
        screen = Builder.load_file('Main.kv')
        return screen
LabelBase.register(
    name="Mphopine", fn_regular="Poppins\\Poppins-Medium.ttf")
LabelBase.register(
    name="Bphopine", fn_regular="Poppins\\Poppins-SemiBold.ttf")
DemoApp().run()

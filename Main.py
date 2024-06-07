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
GOOGLE_CLIENT_ID = (
    ""
)
GOOGLE_CLIENT_SECRET = ""

os.environ["SSL_CERT_FILE"] = certifi.where()
if platform == "android":
    # from android.runnable import run_on_ui_thread
    from jnius import autoclass, cast

    Toast = autoclass("android.widget.Toast")
    String = autoclass("java.lang.String")
    CharSequence = autoclass("java.lang.CharSequence")
    Intent = autoclass("android.content.Intent")
    Uri = autoclass("android.net.Uri")
    NewRelic = autoclass("com.newrelic.agent.android.NewRelic")
    LayoutParams = autoclass("android.view.WindowManager$LayoutParams")
    AndroidColor = autoclass("android.graphics.Color")

    PythonActivity = autoclass("org.kivy.android.PythonActivity")

    context = PythonActivity.mActivity

    def show_toast(text):
        t = Toast.makeText(
            context, cast(CharSequence, String(text)), Toast.LENGTH_SHORT
        )
        t.show()

    # @run_on_ui_thread
    def set_statusbar_color():
        window = context.getWindow()
        window.addFlags(LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
        window.setStatusBarColor(AndroidColor.TRANSPARENT)


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


cred = credentials.Certificate('Firebase.json')
# gets access to firestore
app = firebase_admin.initialize_app(cred)
db = firestore.client()
User_id_12 = ""
config = {
    "apiKey": "AIzaSyDiSiQcmuTEHdHUio2tOprPOX65MJ8SkMk",
    "authDomain": "test-4d090.firebaseapp.com",
    "databaseURL": "https://test-4d090-default-rtdb.firebaseio.com",

    "projectId": "test-4d090",
    "storageBucket": "test-4d090.appspot.com",
    "messagingSenderId": "1060349065580",
    "appId": "1:1060349065580:web:1ee1a40ea145f1ef9a5b49",
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()


Window.size = (300, 550)


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
            try:

                self.dialog.open()
                user = auth.create_user_with_email_and_password(
                    self.username, self.password)
                
                id = f"{user['localId']}"
                data = {"first_name": self.firstname, "last_name": self.lastname,"broker_localid":id}
                obj = MainScreen()
                obj.User_id_121 = id
                # database.child("users").child(id).set(data)
                db.collection(u'users').document(id).set(data)
                db.collection(u'User_stockes').document(id).set({"Stock1":"","Stock2":""})
                self.dialog.dismiss()
                self.manager.current = 'welcome'
            except:
                pop = pop_up()
                pop.tshow = 'This Email Is already Register'
                pop.show()
                self.dialog.dismiss()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.button_push, 0)
    values_dict = {}

    def Buy(self, obj):
        self.manager.get_screen(
            "fdb").ids.lab_fip.text = f"This Financial Institution Get {self.values_dict[obj]} %"
        # self.manager.get_screen("cart").ids.per.text = f"{self.values_dict[obj]}"
        self.manager.get_screen("cart").ids.per.text = f"{self.values_dict[obj]}"
        # self.manager.get_screen("buysscreen").ids.per.text = f"{self.values_dict[obj]}"
        self.manager.get_screen("fdb").ids.lab_fi.text = obj
        self.manager.current = 'fdb'

    def button_push(self, *args):
        try:
            users_ref = db.collection('financial_institutions').stream()
            # users_ref = db.collection('users')
            docs = users_ref
            for doc in docs:
                self.values_dict[doc.id] = doc.to_dict()["percentage"]
                self.ids.listone.add_widget(OneLineListItem(
                    text=f'{doc.id}', on_press=lambda x: self.Buy(x.text)))
        except:
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
            content_cls=Content(),
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
                user = auth.sign_in_with_email_and_password(
                    self.username, self.password)
                # User_id_12=user['localId']

                f = open("id.txt", "w")
                f.write(user['localId'])
                f.close()
                self.dialog.dismiss()
                self.manager.current = 'main'

        except:
            pop = pop_up()
            pop.tshow = 'you password and Email incorrect'
            pop.show()
            self.dialog.dismiss()


class F1Screen(Screen):
    pass


class FdbScreen(Screen):
    def Broker(self, bo):

        self.manager.get_screen("blist").ids.fibn.text = bo
        self.manager.get_screen("blistg").ids.fibn.text = bo
        if self.manager.get_screen("fdb").ids.lab_fi.text =="Goldman Sachs":

            self.manager.current = 'blistg'
        elif self.manager.get_screen("fdb").ids.lab_fi.text =="Gold Finance":
            self.manager.current = 'blistgf'
        elif self.manager.get_screen("fdb").ids.lab_fi.text =="Cheap Investments":
            self.manager.current = 'blistch'
        else:
            self.manager.current = 'blist'
        
class FdbScreen2(Screen):
    def Broker(self, bo):
        self.manager.get_screen("blist").ids.fibn.text = bo
        self.manager.get_screen("blist").ids.fibn.text = bo
        self.manager.current = 'bdi'

class Brokerlistch(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.button_push, 1)
    values_dict = {}
    values_dict1 = {}

    def Buy(self, obj):

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
            # buttons=[btn],
        )
        self.dialog.open()
        # users_ref = db.collection(u'Sample').document(self.ids.fibn.text).get()
        users_ref = db.collection(u'Sample').document(f'Cheap Investments').get()
            # users_ref = db.collection('users')
        docs = users_ref.to_dict()
            
            # for doc in docs:
                # print(f"{doc.id} ==> {doc.to_dict()}")
                # self.values_dict[doc.id]=doc.to_dict()["value"]
        for item in docs:
            d1=docs[item]
            if d1[0]==obj:
                name=d1[0]
                email=d1[2]
            
        self.manager.get_screen("bdi").ids.name.text = f"{name}"
        self.manager.get_screen("bdi").ids.email.text = f"{email}"
        
        self.dialog.dismiss()
        
        self.manager.current = 'fdb2'
        # self.manager.current = 'fdb2'

    def pusing(self):
        Clock.schedule_once(self.button_push, 0)
        

    def button_push(self,*arg):
        try:
            users_ref = db.collection(u'Sample').document(f'Cheap Investments').get()

            docs = users_ref.to_dict()

            for item in docs:
                d1=docs[item]
                das1=d1[0]
                self.ids.list_two.add_widget(OneLineListItem(text=f'{das1}', on_press=lambda x: self.Buy(x.text)))
        except:
            pass



class Brokerlistgold(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.button_push, 1)
    values_dict = {}
    values_dict1 = {}

    def Buy(self, obj):

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
            # buttons=[btn],
        )
        self.dialog.open()
        # users_ref = db.collection(u'Sample').document(self.ids.fibn.text).get()
        users_ref = db.collection(u'Sample').document(f'Goldman Sachs').get()
            # users_ref = db.collection('users')
        docs = users_ref.to_dict()
            
            # for doc in docs:
                # print(f"{doc.id} ==> {doc.to_dict()}")
                # self.values_dict[doc.id]=doc.to_dict()["value"]
        for item in docs:
            d1=docs[item]
            if d1[0]==obj:
                name=d1[0]
                email=d1[2]
            
        self.manager.get_screen("bdi").ids.name.text = f"{name}"
        self.manager.get_screen("bdi").ids.email.text = f"{email}"
        
        self.dialog.dismiss()
        
        self.manager.current = 'fdb2'
        # self.manager.current = 'fdb2'

    def pusing(self):
        Clock.schedule_once(self.button_push, 0)
        

    def button_push(self,*arg):
        try:
            users_ref = db.collection(u'Sample').document(f'Goldman Sachs').get()

            docs = users_ref.to_dict()

            for item in docs:
                d1=docs[item]
                das1=d1[0]
                self.ids.list_two.add_widget(OneLineListItem(text=f'{das1}', on_press=lambda x: self.Buy(x.text)))
        except:
            pass
class Brokerlistgoldf(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.button_push, 1)
    values_dict = {}
    values_dict1 = {}

    def Buy(self, obj):

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
            # buttons=[btn],
        )
        self.dialog.open()
        # users_ref = db.collection(u'Sample').document(self.ids.fibn.text).get()
        users_ref = db.collection(u'Sample').document(f'Gold Finance').get()
            # users_ref = db.collection('users')
        docs = users_ref.to_dict()
            
            # for doc in docs:
                # print(f"{doc.id} ==> {doc.to_dict()}")
                # self.values_dict[doc.id]=doc.to_dict()["value"]
        for item in docs:
            d1=docs[item]
            if d1[0]==obj:
                name=d1[0]
                email=d1[2]
            
        self.manager.get_screen("bdi").ids.name.text = f"{name}"
        self.manager.get_screen("bdi").ids.email.text = f"{email}"
        
        self.dialog.dismiss()
        
        self.manager.current = 'fdb2'
        # self.manager.current = 'fdb2'

    def pusing(self):
        Clock.schedule_once(self.button_push, 0)
        

    def button_push(self,*arg):
        try:
            users_ref = db.collection(u'Sample').document(f'Gold Finance').get()

            docs = users_ref.to_dict()

            for item in docs:
                d1=docs[item]
                das1=d1[0]
                self.ids.list_two.add_widget(OneLineListItem(text=f'{das1}', on_press=lambda x: self.Buy(x.text)))
        except:
            pass

class Brokerlist(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.button_push, 1)
    values_dict = {}
    values_dict1 = {}

    def Buy(self, obj):

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
            # buttons=[btn],
        )
        self.dialog.open()
        # users_ref = db.collection(u'Sample').document(self.ids.fibn.text).get()
        users_ref = db.collection(u'Sample').document(f'TopG FinInst').get()
            # users_ref = db.collection('users')
        docs = users_ref.to_dict()
            
            # for doc in docs:
                # print(f"{doc.id} ==> {doc.to_dict()}")
                # self.values_dict[doc.id]=doc.to_dict()["value"]
        for item in docs:
            d1=docs[item]
            if d1[0]==obj:
                name=d1[0]
                email=d1[2]
            
        self.manager.get_screen("bdi").ids.name.text = f"{name}"
        self.manager.get_screen("bdi").ids.email.text = f"{email}"
        
        self.dialog.dismiss()

        self.manager.current = 'fdb2'

    def pusing(self):
        Clock.schedule_once(self.button_push, 0)
        

    def button_push(self,*arg):
        try:
            # users_ref  = db.collection(u'fibroker').document(self.ids.fibn.text).get()
            print(self.ids.fibn.text)
            users_ref = db.collection(u'Sample').document(f'TopG FinInst').get()

            # users_ref = db.collection('users')
            docs = users_ref.to_dict()
            # for doc in docs:
            #     print(f"{doc.id} ==> {doc.to_dict()}")
                # self.values_dict[doc.id]=doc.to_dict()["value"]
            for item in docs:
                d1=docs[item]
                das1=d1[0]
                self.ids.list_two.add_widget(OneLineListItem(text=f'{das1}', on_press=lambda x: self.Buy(x.text)))
        except:
            pass

class PurchaseScreen1(Screen):
    def buyingcoin(self):
        oper = True
        if len(self.cn) == 0:
            oper = False
            pop = pop_up()
            pop.tshow = 'Card Number Field is Empty'
            pop.show()
        else:
            if len(self.chn) == 0:
                oper = False
                pop = pop_up()
                pop.tshow = 'Card Holder Name Field is Empty'
                pop.show()
            else:
                if len(self.expiry) == 0:
                    oper = False
                    pop = pop_up()
                    pop.tshow = 'Expiry Date Field  is Empty'
                    pop.show()
                else:
                    if len(self.cvv) == 0:
                        oper = False
                        pop = pop_up()
                        pop.tshow = 'Password Field is Empty'
                        pop.show()
        if oper:
            f = open("id.txt", "r")
            d = f.read()
            f.close()
            users_ref = db.collection(u'User_stockes').document(f'{d}').get()
            data = users_ref.to_dict()
            if len(data["Stock1"]) == 0 or len(data["Stock2"]) == 0:
                if len(data["Stock1"]) == 0:
                    data1 = {u"Stock1": f"{self.ids.stock.text}",
                             u"Stock2": data["Stock2"]}
                    pop = pop_up()
                    pop.tshow = 'Stock Is Buyed'
                    pop.show()
                    db.collection(u'User_stockes').document(f"{d}").set(data1)
                    self.manager.current = 'main'
                else:

                    data1 = {u"Stock1": data["Stock1"],
                             u"Stock2": f"{self.ids.stock.text}"}
                    db.collection(u'User_stockes').document(f"{d}").set(data1)

                    pop = pop_up()
                    pop.tshow = 'Stock Is Buyed'
                    pop.show()

                    self.manager.current = 'main'

            else:
                pop = pop_up()
                pop.tshow = 'You Have ALso Buy 2 stockes'
                pop.show()

class Brokerdetails(Screen):
    def open_email(self):
        webbrowser.open(f"mailto:{self.ids.email.text}?subject=Nice%20App&body=You're%20hired")


class F2Screen(Screen):
    pass


class F3Screen(Screen):
    pass


class F4Screen(Screen):
    pass


class CryptoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.button_push, 0)
    values_dict = {}

    def Buy(self, obj):

        self.manager.get_screen(
            "buyscreen3").ids.value.text = f"The price of Coin is {self.values_dict[obj]}$"
        self.manager.get_screen("buyscreen3").ids.result.text = obj
        self.manager.current = 'buyscreen3'

    def button_push(self, *args):
        
        try:

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
                # buttons=[btn],
            )
            self.dialog.open()

            users_ref = db.collection('crypto').get()
            # users_ref = db.collection('users')
            docs = users_ref
            for doc in docs:

                # print(f"{doc.id} ==> {doc.to_dict()}")
                v=doc.to_dict()
                res = list(v.values())[0]
                self.values_dict[doc.id] = res 
                self.ids.list_one.add_widget(OneLineListItem(text=f'{doc.id}', on_press=lambda x: self.Buy(x.text)))
            self.dialog.dismiss()
        except:
            self.dialog.dismiss()


class CryptoBuy_1Screen(Screen):
    pass


class CryptoBuy_2Screen(Screen):
    pass


class CryptoBuy_3Screen(Screen):
    pass


class CryptoBuy_4Screen(Screen):
    pass


class F1b1Screen(Screen):
    pass


class F1b2Screen(Screen):
    pass


class F2b1Screen(Screen):
    pass


class F3b1Screen(Screen):
    pass


class F3b2Screen(Screen):
    pass


class F4b1Screen(Screen):
    pass


class F1bScreen(Screen):
    pass


class F2bScreen(Screen):
    pass


class F3bScreen(Screen):
    pass


class F4bScreen(Screen):
    pass


class SupportScreen(Screen):
    pass


class ReviewScreen(Screen):
    star = 0

    def start1(self):
        self.ids.Stars.text = "Star 1/5"
        self.star = 1

    def start2(self):
        self.ids.Stars.text = "Star 2/5"
        self.star = 2

    def start3(self):
        self.ids.Stars.text = "Star 3/5"
        self.star = 3

    def start4(self):
        self.ids.Stars.text = "Star 4/5"
        self.star = 4

    def start5(self):
        self.ids.Stars.text = "Star 5/5"
        self.star = 5

    def send_data(self):
        if self.star == 0:
            pop = pop_up()
            pop.tshow = 'Please Select Star from Option 1 to 5'
            pop.show()
        else:
            f = open("id.txt", "r")
            d = f.read()
            f.close()
            users_ref  = db.collection(u'users').document(d).get()

            data_1 = users_ref.to_dict()
            data = {"Name": data_1["first_name"],
                    "Rating": f"{self.star}"+"/5", "Review": self.rev}
            db.collection(u'Review').document(d).set(data)
            pop = pop_up2()
            pop.tshow = 'Thank U for Review'
            pop.show()


class F1d1Screen(Screen):
    pass


class F1d2Screen(Screen):
    pass


class F2d1Screen(Screen):
    pass


class F3d1Screen(Screen):
    pass


class F3d2Screen(Screen):
    pass


class F4d1Screen(Screen):
    pass


class CartScreen(Screen):
    def plus(self):        
        self.ids.num.text=f"{int(self.ids.num.text)+1}"
        
        self.ids.total.text=f"{int(self.ids.num.text)*int(self.ids.Price.text) +(int(self.ids.num.text)*int(self.ids.Price.text)*float(self.ids.per.text))  }"
    def minus(self):
        if int(self.ids.num.text)==0:
            self.ids.num.text="0"
            self.ids.total.text="0"

        else:
            self.ids.num.text=f"{int(self.ids.num.text)-1}"
            self.ids.total.text=f"{int(self.ids.num.text)*int(self.ids.Price.text)}"
class CartScreen2(Screen):
    def plus(self):        
        self.ids.num.text=f"{int(self.ids.num.text)+1}"
        
        self.ids.total.text=f"{int(self.ids.num.text)*int(self.ids.Price.text)  }"
    def minus(self):
        if int(self.ids.num.text)==0:
            self.ids.num.text="0"
            self.ids.total.text="0"

        else:
            self.ids.num.text=f"{int(self.ids.num.text)-1}"
            self.ids.total.text=f"{int(self.ids.num.text)*int(self.ids.Price.text)}"
class CartScreen1(Screen):
    def plus(self):        
        self.ids.num.text=f"{int(self.ids.num.text)+1}"
        
        self.ids.total.text=f"{int(self.ids.num.text)*int(self.ids.Price.text)   }"
    def minus(self):
        if int(self.ids.num.text)==0:
            self.ids.num.text="0"
            self.ids.total.text="0"

        else:
            self.ids.num.text=f"{int(self.ids.num.text)-1}"
            self.ids.total.text=f"{int(self.ids.num.text)*int(self.ids.Price.text)}"


class PurchaseScreen3(Screen):
    def buyingcoin(self):
        oper = True
        if len(self.cn) == 0:
            oper = False
            pop = pop_up()
            pop.tshow = 'Card Number Field is Empty'
            pop.show()
        else:
            if len(self.chn) == 0:
                oper = False
                pop = pop_up()
                pop.tshow = 'Card Holder Name Field is Empty'
                pop.show()
            else:
                if len(self.expiry) == 0:
                    oper = False
                    pop = pop_up()
                    pop.tshow = 'Expiry Date Field  is Empty'
                    pop.show()
                else:
                    if len(self.cvv) == 0:
                        oper = False
                        pop = pop_up()
                        pop.tshow = 'Cvv Field is Empty'
                        pop.show()
        if oper:
            f = open("id.txt", "r")
            d = f.read()
            f.close()
            
            d= self.manager.get_screen("fdb").ids.lab_fi.text
            users_ref = db.collection('financial_institutions').doc
            # users_ref = db.collection('users')
            users_ref  = db.collection(u'financial_institutions').document(d).get()
            data=users_ref.to_dict()
            per=data["percentage"]
            
            
            
class PurchaseScreen(Screen):
    def buyingcoin(self):
        oper = True
        if len(self.cn) == 0:
            oper = False
            pop = pop_up()
            pop.tshow = 'Card Number Field is Empty'
            pop.show()
        else:
            if len(self.chn) == 0:
                oper = False
                pop = pop_up()
                pop.tshow = 'Card Holder Name Field is Empty'
                pop.show()
            else:
                if len(self.expiry) == 0:
                    oper = False
                    pop = pop_up()
                    pop.tshow = 'Expiry Date Field  is Empty'
                    pop.show()
                else:
                    if len(self.cvv) == 0:
                        oper = False
                        pop = pop_up()
                        pop.tshow = 'Password Field is Empty'
                        pop.show()
        if oper:
            f = open("id.txt", "r")
            d = f.read()
            f.close()
            users_ref = db.collection(u'User_stockes').document(f'{d}').get()
            data = users_ref.to_dict()
            if len(data["Stock1"]) == 0 or len(data["Stock2"]) == 0:
                if len(data["Stock1"]) == 0:
                    data1 = {u"Stock1": f"{self.ids.stock.text}",
                             u"Stock2": data["Stock2"]}
                    pop = pop_up()
                    pop.tshow = 'Stock Is Buyed'
                    pop.show()
                    db.collection(u'User_stockes').document(f"{d}").set(data1)
                    self.manager.current = 'main'
                else:

                    data1 = {u"Stock1": data["Stock1"],
                             u"Stock2": f"{self.ids.stock.text}"}
                    db.collection(u'User_stockes').document(f"{d}").set(data1)

                    pop = pop_up()
                    pop.tshow = 'Coin Is Buyed'
                    pop.show()

                    self.manager.current = 'main'

            else:
                pop = pop_up()
                pop.tshow = 'You Have ALso Buy 2 stockes'
                pop.show()

class PurchaseScreen2(Screen):
    def buyingcoin(self):
        oper = True
        if len(self.cn) == 0:
            oper = False
            pop = pop_up()
            pop.tshow = 'Card Number Field is Empty'
            pop.show()
        else:
            if len(self.chn) == 0:
                oper = False
                pop = pop_up()
                pop.tshow = 'Card Holder Name Field is Empty'
                pop.show()
            else:
                if len(self.expiry) == 0:
                    oper = False
                    pop = pop_up()
                    pop.tshow = 'Expiry Date Field  is Empty'
                    pop.show()
                else:
                    if len(self.cvv) == 0:
                        oper = False
                        pop = pop_up()
                        pop.tshow = 'Password Field is Empty'
                        pop.show()
        if oper:
            f = open("id.txt", "r")
            d = f.read()
            f.close()
            users_ref = db.collection(u'User_Stock5').document(f'{d}').get()
            data = users_ref.to_dict()
            if len(data["Stock1"]) == 0 or len(data["Stock2"]) == 0 or len(data["Stock3"]) == 0 or len(data["Stock4"]) == 0 or len(data["Stock5"]) == 0:
                if len(data["Stock1"]) == 0:
                    data1 = {u"Stock1": self.ids.stock.text,
                             u"Stock2": data["Stock2"],
                             u"Stock3": data["Stock3"],
                             u"Stock4": data["Stock4"],
                             u"Stock5": data["Stock5"]
                             }
                    pop = pop_up()
                    pop.tshow = 'Stock Is Buyed'
                    pop.show()
                    db.collection(u'User_Stock5').document(f"{d}").set(data1)
                    self.manager.current = 'main'
                elif len(data["Stock2"]) == 0:
                    data1 = {u"Stock1": data["Stock1"],
                             u"Stock2": f"{self.ids.stock.text}",
                             u"Stock3": data["Stock3"],
                             u"Stock4": data["Stock4"],
                             u"Stock5": data["Stock5"]
                             }
                    pop = pop_up()
                    pop.tshow = 'Stock Is Buyed'
                    pop.show()
                    db.collection(u'User_Stock5').document(f"{d}").set(data1)
                    self.manager.current = 'main' 
                elif len(data["Stock3"]) == 0:
                    data1 = {u"Stock1": data["Stock1"],
                             u"Stock2": data["Stock2"],
                             u"Stock3": f"{self.ids.stock.text}",
                             u"Stock4": data["Stock4"],
                             u"Stock5": data["Stock5"]
                             }
                    pop = pop_up()
                    pop.tshow = 'Stock Is Buyed'
                    pop.show()
                    db.collection(u'User_Stock5').document(f"{d}").set(data1)
                    self.manager.current = 'main'
                elif len(data["Stock4"]) == 0:
                    data1 = {u"Stock1": data["Stock1"],
                             u"Stock2": data["Stock2"],
                             u"Stock3": data["Stock3"],
                             u"Stock4": f"{self.ids.stock.text}",
                             u"Stock5": data["Stock5"]
                             }
                    pop = pop_up()
                    pop.tshow = 'Stock Is Buyed'
                    pop.show()
                    db.collection(u'User_Stock5').document(f"{d}").set(data1)
                    self.manager.current = 'main'
                
                else:
                    data1 = {u"Stock1": data["Stock1"],
                             u"Stock2": data["Stock2"],
                             u"Stock3": data["Stock3"],
                             u"Stock4": data["Stock5"],
                             u"Stock5": f"{self.ids.stock.text}"
                             }
                    pop = pop_up()
                    pop.tshow = 'Stock Is Buyed'
                    pop.show()
                    db.collection(u'User_Stock5').document(f"{d}").set(data1)

                    

                    self.manager.current = 'main'

            else:
                pop = pop_up()
                pop.tshow = 'You Have ALso Buy 5 Stockes'
                pop.show()

class Welcome(Screen):
    pass


class Content(Screen):
    pass
class BuyScreen3(Screen):
    def pur(self):
        self.manager.get_screen("purchase").ids.stock.text = self.ids.result.text
        self.manager.get_screen("cart2").ids.fibn.text = self.ids.result.text
        self.manager.current='cart2'

class BuyScreen(Screen):
    def pur(self):
        self.manager.get_screen("purchase2").ids.stock.text = self.ids.result.text
        self.manager.get_screen("cart1").ids.fibn.text = self.ids.result.text
        self.manager.current='cart1'
        
class BuySScreen(Screen):
    def pur(self):
        self.manager.get_screen("purchase2").ids.stock.text = self.ids.result.text
        self.manager.get_screen("cart").ids.fibn.text = self.ids.result.text
        self.manager.current='cart1'
class Contact(Screen):
    def send_data(self):
        data = {"Name": self.name1, "Email": self.email, "Problem": self.msg}
        f = open("id.txt", "r")
        d = f.read()
        f.close()
        db.collection(u'Contact').document(d).set(data)
        pop = pop_up2()
        pop.tshow = 'We Contact You As Soon as Possiable'
        pop.show()
class StockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.button_push, 0)
    values_dict = {}

    def Buy(self, obj):
        val=float(self.ids.result.text)+float(self.manager.get_screen("cart1").ids.per.text)
        self.manager.get_screen(
            "buyscreen").ids.value.text = f"The price is {val}"
        # self.manager.get_screen("buyscreen").ids.result.text = obj
        print(self.values_dict[obj])
        self.manager.get_screen("cart1").ids.Price.text = f"{self.values_dict[obj]}"
        self.manager.get_screen("cart2").ids.Price.text = f"{self.values_dict[obj]}"
        self.manager.current = 'buyscreen'
        # self.manager.current = 'fdb2'
    def button_push(self, *args):
        
        try:

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
                # buttons=[btn],
            )
            self.dialog.open()

            users_ref = db.collection('stock').get()
            # users_ref = db.collection('users')
            docs = users_ref
            for doc in docs:

                # print(f"{doc.id} ==> {doc.to_dict()}")
                v=doc.to_dict()
                res = list(v.values())[0]
                self.values_dict[doc.id] = res 
                self.ids.list_two.add_widget(OneLineListItem(text=f'{doc.id}', on_press=lambda x: self.Buy(x.text)))
            self.dialog.dismiss()
        except:
            self.dialog.dismiss()
class StockScreen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.button_push, 0)
    values_dict = {}

    def Buy(self, obj):
        val=float(self.values_dict[obj])+float(self.manager.get_screen("cart").ids.per.text )
        # self.manager.get_screen(
        #     "buyscreen").ids.value.text = f"The price is {self.values_dict[obj]}"
        self.manager.get_screen(
            "buysscreen").ids.value.text = f"The price is {val} $"
        # self.manager.get_screen("cart").ids.Price.text = f"{self.values_dict[obj]}"
        self.manager.get_screen("cart1").ids.Price.text = f"{val}"
        self.manager.get_screen("cart2").ids.Price.text = f"{val}"
        
        # print(self.values_dict[obj])
        self.manager.get_screen("buysscreen").ids.result.text = obj
        self.manager.current = 'buysscreen'
        

    def button_push(self, *args):
        
        try:

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
                # buttons=[btn],
            )
            self.dialog.open()

            users_ref = db.collection('stock').get()
            # users_ref = db.collection('users')
            docs = users_ref
            for doc in docs:

                # print(f"{doc.id} ==> {doc.to_dict()}")
                v=doc.to_dict()
                res = list(v.values())[0]
                self.values_dict[doc.id] = res 
                self.ids.list_three.add_widget(OneLineListItem(text=f'{doc.id}', on_press=lambda x: self.Buy(x.text)))
            self.dialog.dismiss()
        except:
            self.dialog.dismiss()

# Create the screen manager
sm = ScreenManager()
sm.add_widget(Welcome(name='welcome'))

sm.add_widget(MainScreen(name='main'))


sm.add_widget(CartScreen(name='cart'))
sm.add_widget(CartScreen1(name='cart1'))
sm.add_widget(CartScreen2(name='cart2'))


sm.add_widget(Brokerlistgold(name='blistg'))
sm.add_widget(Brokerlistch(name='blistch'))
sm.add_widget(Brokerlistgoldf(name='blistgf'))


sm.add_widget(StockScreen(name='stock'))
sm.add_widget(StockScreen2(name='stock2'))


sm.add_widget(Brokerlist(name='blist'))

sm.add_widget(ReviewScreen(name='review'))
sm.add_widget(CryptoScreen(name='crypto'))
sm.add_widget(BuyScreen(name='buyscreen'))
sm.add_widget(BuySScreen(name='buysscreen'))
sm.add_widget(BuyScreen3(name='buyscreen3'))


sm.add_widget(Contact(name='contact'))

sm.add_widget(Content(name='content'))

sm.add_widget(FirstScreen(name='first'))
sm.add_widget(CreateScreen(name='create'))

sm.add_widget(LoginScreen(name='login'))
sm.add_widget(F1Screen(name='f1'))
sm.add_widget(FdbScreen(name='fdb'))
sm.add_widget(FdbScreen2(name='fdb2'))

sm.add_widget(Brokerdetails(name='bdi'))

sm.add_widget(F2Screen(name='f2'))
sm.add_widget(F3Screen(name='f3'))
sm.add_widget(F4Screen(name='f4'))


sm.add_widget(CryptoScreen(name='crypto'))
sm.add_widget(CryptoBuy_1Screen(name='cb1'))
sm.add_widget(CryptoBuy_2Screen(name='cb2'))
sm.add_widget(CryptoBuy_3Screen(name='cb3'))
sm.add_widget(CryptoBuy_4Screen(name='cb4'))
sm.add_widget(F1b1Screen(name='f1b1'))
sm.add_widget(F1b2Screen(name='f1b2'))
sm.add_widget(F2b1Screen(name='f2b1'))
sm.add_widget(F3b1Screen(name='f3b1'))
sm.add_widget(F3b2Screen(name='f3b2'))
sm.add_widget(F4b1Screen(name='f4b1'))
sm.add_widget(F1bScreen(name='f1b'))
sm.add_widget(F1bScreen(name='f2b'))
sm.add_widget(F1bScreen(name='f3b'))
sm.add_widget(F1bScreen(name='f4b'))
sm.add_widget(SupportScreen(name='support'))


sm.add_widget(F1d1Screen(name='f1d1'))
sm.add_widget(F1d2Screen(name='f1d2'))
sm.add_widget(F2d1Screen(name='f2d1'))
sm.add_widget(F3d1Screen(name='f3d1'))
sm.add_widget(F3d2Screen(name='f3d2'))
sm.add_widget(F4d1Screen(name='f4d1'))




sm.add_widget(PurchaseScreen(name='purchase'))
sm.add_widget(PurchaseScreen1(name='purchase1'))
sm.add_widget(PurchaseScreen2(name='purchase2'))
sm.add_widget(PurchaseScreen3(name='purchase3'))




class DemoApp(MDApp):

    def build(self):
        initialize_google(
            self.after_login,
            self.error_listener,


            "",
            ""
        )
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        screen = Builder.load_file('Main.kv')
        if platform != "android":
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.button import MDFlatButton

            btn = MDFlatButton(
                text="CANCEL", text_color=self.theme_cls.primary_color)
            btn.bind(on_release=lambda *args: (stop_login(), self.dialog.dismiss()))
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
        return screen

    def on_start(self):
        pass

    def show_login_progress(self):
        if platform != "android":
            self.dialog.open()

    def hide_login_progress(self):
        if platform != "android":
            self.dialog.dismiss()

    def gl_login(self, *args):
        if platform != "android":
            self.dialog.open()
        login_google()
        self.current_provider = login_providers.google

        self.show_login_progress()

    def logout_(self):

        if self.current_provider == login_providers.google:
            logout_google(self.after_logout)

    def after_login(self, name, email, photo_uri):
        self.hide_login_progress()

        if platform == "android":
            show_toast("Logged in using {}".format(self.current_provider))
        else:
            self.root.current = "main"
            Snackbar(text="Logged in using {}".format(
                self.current_provider)).show()

        self.update_ui(name, email, photo_uri)
        self.root.current = "main"

    def after_logout(self):
        # self.update_ui("", "", "")
        self.root.current = "FirstScreen"
        if platform == "android":
            show_toast(text="Logged out from {} login".format(
                self.current_provider))
        else:
            Snackbar(
                text="Logged out from {} login".format(self.current_provider)
            ).show()

    def update_ui(self, name, email, photo_uri):

        print(name)

    def error_listener(self):
        if platform == "android":
            show_toast("Error logging in.")
        else:
            Snackbar(text="Error logging in. Check connection or try again.").show()
        Clock.schedule_once(lambda *args: self.hide_login_progress())


LabelBase.register(
    name="Mphopine", fn_regular="Poppins\\Poppins-Medium.ttf")
LabelBase.register(
    name="Bphopine", fn_regular="Poppins\\Poppins-SemiBold.ttf")

DemoApp().run()

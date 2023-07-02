
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRaisedButton


from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

from kivy.properties import ObjectProperty , BooleanProperty
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.clock import Clock


class TourerScreen(BoxLayout):
	pass

class TourerActivity(BoxLayout):
	talking = BooleanProperty(True)
	start_tour = BooleanProperty(False)


class CustomActionButton(MDRaisedButton):
	pass
	
class ActionList(ScrollView):
	button_list : MDGridLayout = ObjectProperty()


class MainWindow(FloatLayout):
	tourer_screen : TourerScreen = ObjectProperty()
	tourer_activity : TourerActivity = ObjectProperty()
	action_list : ActionList = ObjectProperty()
	
	title_1 : Label = ObjectProperty()
	title_2 : Label = ObjectProperty()
	
	
	def on_kv_post(self , _ ):
		Clock.schedule_interval(self.update , 1 / 30)
	
	def update(self , _ ):
		# remove TourerScreen if not talking
		self.tourer_screen.opacity = 0 if not self.tourer_activity.talking else 1
		
		# show the ActionList when user start touring
		self.action_list.opacity = 1 if self.tourer_activity.start_tour else 0
		
		# remove title when talking or start tour
		if not self.tourer_activity.start_tour :
			self.title_1.opacity = 0 if self.tourer_activity.talking else 1
			self.title_2.opacity = 0 if self.tourer_activity.talking else 1
		else:
			if self.title_1.opacity :
				self.title_1.opacity = 0
				self.title_2.opacity = 0
			

class OCTourApp(MDApp):
	
	def build(self):
		return Builder.load_file("design.kv")



LabelBase.register(name = "font_Obli" , fn_regular="fonts/Quicksand_Bold_Oblique.otf")
LabelBase.register(name = "font_bold" , fn_regular="fonts/Quicksand_Bold.otf")
LabelBase.register(name = "font_book" , fn_regular="fonts/Quicksand_Book_Oblique.otf")
LabelBase.register(name = "font_book_reg" , fn_regular="fonts/Quicksand_Book.otf")
LabelBase.register(name = "azonix" , fn_regular="fonts/Azonix.otf")
LabelBase.register(name = "font_light_Obli" , fn_regular="fonts/Quicksand_Light_Oblique.otf")

OCTourApp().run()

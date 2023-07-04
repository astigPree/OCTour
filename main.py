
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRaisedButton


from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.effectwidget import EffectWidget

from kivy.properties import ObjectProperty , BooleanProperty, StringProperty , NumericProperty , DictProperty , ListProperty 
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.clock import Clock

import json
import random
import os

class TourerScreen(BoxLayout):
	name_holder : Label = ObjectProperty()
	dialog : Label = ObjectProperty()
	tourer_picture : Image = ObjectProperty()
	
	def update(self , name_holder = None , dialog = None , picture = None):
		if name_holder :
			self.name_holder.text = name_holder
		if dialog:
			self.dialog.text = dialog
		if picture:
			self.tourer_picture.source = picture


class TourerActivity(BoxLayout):
	talking = BooleanProperty(True)
	start_tour = BooleanProperty(False)
	start_acitivity : callable = ObjectProperty()


class CustomActionButton(MDRaisedButton):
	activity : callable = ObjectProperty()
	
	
class ActionList(ScrollView):
	button_list : MDGridLayout = ObjectProperty()
	
	ready_to_change = BooleanProperty(False)
	parent_activity : callable = ObjectProperty()
	
	def update(self , rooms : list[str , ...]):
		self.button_list.clear_widgets()
		for room in rooms :
			widget = CustomActionButton()
			widget.text = room
			widget.activity = self.action
			self.button_list.add_widget(widget)
	
	def action(self , text : str):
		def ready_to_change( _ ):
			self.ready_to_change = False
		
		if not self.ready_to_change:
			Clock.schedule_once(ready_to_change , 0.2)
			self.parent_activity(text)
			

class MainWindow(FloatLayout):
	tourer_screen : TourerScreen = ObjectProperty()
	tourer_activity : TourerActivity = ObjectProperty()
	action_list : ActionList = ObjectProperty()
	
	building_picture : EffectWidget = ObjectProperty()
	size_effect = NumericProperty(8.0)
	
	title_1 : Label = ObjectProperty()
	title_2 : Label = ObjectProperty()
	
	buidings_info : dict = ObjectProperty({})
	selections : dict = ObjectProperty({})
	tourers : list = ObjectProperty([])
	
	def on_kv_post(self , _ ):
		#Clock.schedule_once(self.load_all_data )
		Clock.schedule_interval(self.update , 1 / 30)
		
	def load_all_data(self , _ ):
		# set the Command In Action List and Tourer Activity
		self.action_list.parent_activity = self.change_location
		self.tourer_activity.start_acitivity = self.change_location
		
		# display the Mahogany Building
		self.update_display_image( image=os.path.join("Rooms", "Building.jpeg"))
		
		# load tourers in update the TourerScreen
		filename = ""
		with open(filename , "r") as jf:
			for tourer in json.load(jf):
				self.tourers.append(tourer)
		tourer = random.choices(self.tourers , k= 1 , cum_weights=[40 , 20 , 20 , 20])
		self.tourer_screen.update(name_holder=tourer["name"] , dialog=tourer["introduction"] , picture=tourer["picture"] )
		
		# load Selection Building 
		filename = ""
		with open( filename , "r") as jf :
			for key , values in json.load(jf).items() :
				self.selections[key] = values
		
		# load Building Information
		filename = ""
		with open( filename , "r") as jf :
			for key , values in json.load(jf).items() :
				self.buidings_info[key] = values
		
	def update(self , _ ):
		# remove TourerScreen if not talking
		self.tourer_screen.opacity = 0 if not self.tourer_activity.talking else 1
		
		# remove title when talking
		if not self.tourer_activity.start_tour :
			self.title_1.opacity = 0 if self.tourer_activity.talking else 1
			self.title_2.opacity = 0 if self.tourer_activity.talking else 1
			
		# MAIN ACTIVITY
		if self.tourer_activity.start_tour:
			
			# blur the image when tourer talking
			self.size_effect = 8.0 if self.tourer_activity.talking else 0.0
			
			# remove title when start tour
			if self.title_1.opacity :
				self.title_1.opacity = 0
				self.title_2.opacity = 0
			
			# show the ActionList when user start touring
			if not self.action_list.opacity :
				self.action_list.opacity = 1
	
	def update_display_image(self , image : str):
		folder = ""
		self.building_picture.picture.source = os.path.join(folder , self.buidings_info[image][0])
	
	def change_location(self , location : str):
		self.update_display_image(location)
		self.tourer_screen.update(dialog=self.buidings_info[location][1])
		self.action_list.update(rooms=self.selections[location])
		

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

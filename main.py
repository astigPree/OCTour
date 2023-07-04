
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRaisedButton


from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image

from kivy.properties import ObjectProperty , BooleanProperty, StringProperty
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.clock import Clock


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


class CustomActionButton(MDRaisedButton):
	activity : callable = ObjectProperty()
	
	
class ActionList(ScrollView):
	button_list : MDGridLayout = ObjectProperty()
	
	ready_to_change = BooleanProperty(False)
	current_selected = StringProperty("")
	past_selected = StringProperty("")
	
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
			self.current_selected = text
			Clock.schedule_once(ready_to_change , 0.2)


class MainWindow(FloatLayout):
	tourer_screen : TourerScreen = ObjectProperty()
	tourer_activity : TourerActivity = ObjectProperty()
	action_list : ActionList = ObjectProperty()
	
	title_1 : Label = ObjectProperty()
	title_2 : Label = ObjectProperty()
	
	def on_kv_post(self , _ ):
		#self.action_list.update(["room 151" , "room 161"])
		Clock.schedule_interval(self.update , 1 / 30)
	
	def introduction(self , _ ):
		pass
	
	def update(self , _ ):
		# remove TourerScreen if not talking
		self.tourer_screen.opacity = 0 if not self.tourer_activity.talking else 1
		
		# remove title when talking
		if not self.tourer_activity.start_tour :
			self.title_1.opacity = 0 if self.tourer_activity.talking else 1
			self.title_2.opacity = 0 if self.tourer_activity.talking else 1
			
		
		# MAIN ACTIVITY
		if self.tourer_activity.start_tour:
			
			# remove title when start tour
			if self.title_1.opacity :
				self.title_1.opacity = 0
				self.title_2.opacity = 0
			
			# show the ActionList when user start touring
			if not self.action_list.opacity :
				self.action_list.opacity = 1
		
		

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

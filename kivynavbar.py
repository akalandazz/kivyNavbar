from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
import kivy.properties as props
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label 
from kivy.graphics import Line
from kivy.core.window import Window
Builder.load_string("""
#:import Window kivy.core.window.Window
#:import get_color_from_hex kivy.utils.get_color_from_hex
<Navbar>
	id:sidenavigation
	BoxLayout:
		orientation:'vertical'
		BoxLayout:
			padding:3
			spacing:10
			canvas.before:
				Color:
					rgba: get_color_from_hex(sidenavigation.navbar_color)
				Rectangle:
					size:self.size
					pos:self.pos
			id:navbar
			size_hint_y:.10
			HumbButton:
				id:humb_bt
				size_hint_x:.1 if Window.width < 500 else .055
				on_press:root.open_navbar(self)
			Label:
				text:"NavigationDrawer"
				font_size:20
			Switch:
				size_hint_x:.15
				on_active:root.change_mode(self)

		BoxLayout:
			id:cont


<SideNav>:
	id:side_nav
	BoxLayout:
		id:nav_content
		spacing:5
		padding:5
		canvas.before:
			Color:
				rgba:get_color_from_hex(root.sidenav_color)
			Rectangle:
				size:self.size
				pos:self.pos
		orientation:'vertical'
		size_hint_x:.80
		Label:
			size_hint:.60,.30
			pos_hint:{'center_x':.5,'center_y':.1}
			canvas:
				Ellipse:
					size:self.size
					pos:self.pos
				Ellipse:
					source:"img4.jpg"
					size:[self.width - 6, self.height - 6]
					pos:[self.x+3,self.y+3]
		Label:
			text:'Choose'
			size_hint_y:.05

		Accordion:
			orientation:'vertical'
			AccordionItem:
				title:'first'
				Button:
					text:'sdsads'
			AccordionItem:
				title:'second'
				Button:
					text:'sdsads'
			AccordionItem:
				title:'third'
				Button:
					text:'sdsads'
	CloseButton:
		id:close_button
		size_hint:.09,.05
		pos_hint:{"center_x":.90, "center_y":.95}
		on_press:root.close_sidebar(self)

            

<CloseButton>:
	opacity:.5 if not self.collide_point(*Window.mouse_pos) else .9
	canvas.before:
		Color:
			rgba:get_color_from_hex(self.bt_color)
		Line:
			points:self.x, self.y, (self.x + self.width), (self.y + self.height)
			width:2 
		Line:
			points:self.x, (self.y+self.height), (self.x + self.width), self.y
			width:2


<HumbButton>:
	opacity:.5 if not self.collide_point(*Window.mouse_pos) else .9
	canvas.before:
		Color:
			rgba:get_color_from_hex(self.humb_color)
		Line:
			points:self.x+5, self.y+10, (self.x + self.width), self.y+10
			width:2 if self.height<45 else 3
		Line:
			points:self.x+5, (self.y+ self.height/2), (self.x + self.width), (self.y+ self.height/2)
			width:2 if self.height<45 else 3
		Line:
			points:self.x+5, (self.y+(self.height-10)), (self.x + self.width), (self.y+ (self.height-10))
			width:2 if self.height<45 else 3

""")
class HumbButton(ButtonBehavior, Label):
	humb_color = props.StringProperty("#FF4141")#Red Color Code, if you see red color it means you got a error



class CloseButton(ButtonBehavior, Label):
	bt_color = props.StringProperty("#FF4141")

class SideNav(FloatLayout):
	sidenav_color = props.StringProperty("#FF4141")


	def close_sidebar(self, *args):
		self.parent.ids.humb_bt.disabled = False
		self.parent.remove_widget(self)

class Navbar(FloatLayout):
	mode = props.OptionProperty("dark", options= ["dark", "light"])
	navbar_color = props.StringProperty("#696969")#Gray Color Code
	sidenav = props.ObjectProperty()

	def __init__(self, **kwargs):
		super(Navbar, self).__init__(**kwargs)
		Clock.schedule_once(self._initiate_navbar, 0)
		Window.bind(on_resize= lambda instance, w,h :setattr(self.sidenav,'width', w/3)) #set sidenav responsive


	def _initiate_navbar(self, *args):
		self.sidenav = SideNav(size_hint_x = None, width = 50)
		if self.mode == "dark":
			self.navbar_color = "#696969"
			self.sidenav.sidenav_color = "#696969"
			self.sidenav.ids.close_button.bt_color = "#EAEAEA"
			self.ids.humb_bt.humb_color = "#EAEAEA"
			

		elif self.mode == "light":
			self.navbar_color = "#EEEDED"
			self.sidenav.sidenav_color ="#EEEDED"
			self.sidenav.ids.close_button.bt_color = "#000000"
			self.ids.humb_bt.humb_color = "#000000"
	

	def open_navbar(self, button):
		self.sidenav.width = 50
		Animation(width = self.width/3, d=.1).start(self.sidenav)
		self.add_widget(self.sidenav)
		button.disabled = True


	def change_mode(self,switch):
		if switch.active:
			self.mode = "light"
		else:
			self.mode = "dark"
		self._initiate_navbar()





class SimpleApp(App):
    def build(self):
        return Navbar()



SimpleApp().run()

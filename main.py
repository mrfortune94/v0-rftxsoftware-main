import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.core.window import Window
from kivy.utils import platform
import threading
import logging

from android_permissions import permissions_manager, request_permissions_on_start

# Import our flasher (will be adapted for Android)
from rftx_flasher_android import BMWFlasher
from tune_matcher import TuneMatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('RFTX.Android')

# Set window size for development (will be full screen on Android)
if platform != 'android':
    Window.size = (360, 640)


class HomeScreen(Screen):
    """Home screen for ECU connection."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flasher = None
        self.build_ui()
        
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='RFTX TUNING',
            size_hint_y=0.1,
            font_size='24sp',
            bold=True,
            color=(0, 0.47, 1, 1)
        )
        layout.add_widget(header)
        
        # Connection section
        conn_layout = GridLayout(cols=2, size_hint_y=0.2, spacing=10)
        conn_layout.add_widget(Label(text='USB Device:', size_hint_x=0.3))
        
        self.port_spinner = Spinner(
            text='Select Device',
            values=['Scanning...'],
            size_hint_x=0.7
        )
        conn_layout.add_widget(self.port_spinner)
        
        self.connect_btn = Button(
            text='Connect',
            size_hint=(1, None),
            height=50,
            background_color=(0, 0.47, 1, 1)
        )
        self.connect_btn.bind(on_press=self.on_connect)
        conn_layout.add_widget(self.connect_btn)
        
        layout.add_widget(conn_layout)
        
        # ECU Info section
        info_label = Label(
            text='ECU Information',
            size_hint_y=0.05,
            font_size='18sp',
            bold=True
        )
        layout.add_widget(info_label)
        
        # ECU info grid
        self.info_grid = GridLayout(cols=2, size_hint_y=0.4, spacing=5)
        
        self.info_labels = {}
        info_fields = ['VIN', 'ECU ID', 'SW Version', 'HW Version', 'ECU Type', 'Bootloader']
        
        for field in info_fields:
            self.info_grid.add_widget(Label(text=f'{field}:', halign='left', size_hint_x=0.4))
            value_label = Label(text='Not connected', halign='left', size_hint_x=0.6)
            self.info_labels[field] = value_label
            self.info_grid.add_widget(value_label)
            
        layout.add_widget(self.info_grid)
        
        # Status label
        self.status_label = Label(
            text='',
            size_hint_y=0.1,
            color=(1, 0.27, 0.27, 1)
        )
        layout.add_widget(self.status_label)
        
        # Navigation buttons
        nav_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        flash_btn = Button(text='Flash', background_color=(0, 0.75, 1, 1))
        flash_btn.bind(on_press=lambda x: self.manager.current = 'flash')
        nav_layout.add_widget(flash_btn)
        
        dtc_btn = Button(text='DTC', background_color=(0, 0.75, 1, 1))
        dtc_btn.bind(on_press=lambda x: self.manager.current = 'dtc')
        nav_layout.add_widget(dtc_btn)
        
        settings_btn = Button(text='Settings', background_color=(0, 0.75, 1, 1))
        settings_btn.bind(on_press=lambda x: self.manager.current = 'settings')
        nav_layout.add_widget(settings_btn)
        
        layout.add_widget(nav_layout)
        
        self.add_widget(layout)
        
        # Schedule port scanning
        Clock.schedule_once(self.scan_ports, 0.5)
        
    def scan_ports(self, dt):
        """Scan for available USB devices."""
        try:
            if platform == 'android':
                from android_usb_serial import get_usb_devices
                devices = get_usb_devices()
                if devices:
                    self.port_spinner.values = [f"{d['name']} ({d['vendor_id']:04x}:{d['product_id']:04x})" for d in devices]
                else:
                    self.port_spinner.values = ['No USB devices found']
            else:
                # Desktop testing
                self.port_spinner.values = ['COM1', 'COM3', '/dev/ttyUSB0']
        except Exception as e:
            logger.error(f"Error scanning ports: {e}")
            self.port_spinner.values = ['Error scanning devices']
            
    def on_connect(self, instance):
        """Handle connect button press."""
        self.status_label.text = 'Connecting...'
        self.connect_btn.disabled = True
        
        # Run connection in background thread
        threading.Thread(target=self.connect_thread, daemon=True).start()
        
    def connect_thread(self):
        """Background thread for connection."""
        try:
            # Get app instance to access shared flasher
            app = App.get_running_app()
            
            if not app.flasher:
                app.flasher = BMWFlasher()
                
            port = self.port_spinner.text
            if app.flasher.connect(port):
                # Read ECU info
                ecu_info = app.flasher.read_ecu_info()
                
                # Update UI on main thread
                Clock.schedule_once(lambda dt: self.update_ecu_info(ecu_info), 0)
            else:
                Clock.schedule_once(lambda dt: self.show_error('Failed to connect to ECU'), 0)
                
        except Exception as e:
            logger.error(f"Connection error: {e}")
            Clock.schedule_once(lambda dt: self.show_error(f'Error: {str(e)}'), 0)
            
        finally:
            Clock.schedule_once(lambda dt: setattr(self.connect_btn, 'disabled', False), 0)
            
    def update_ecu_info(self, ecu_info):
        """Update ECU info labels."""
        self.info_labels['VIN'].text = ecu_info.get('vin', 'Unknown')
        self.info_labels['ECU ID'].text = ecu_info.get('ecu_id', 'Unknown')
        self.info_labels['SW Version'].text = ecu_info.get('sw_version', 'Unknown')
        self.info_labels['HW Version'].text = ecu_info.get('hw_version', 'Unknown')
        self.info_labels['ECU Type'].text = ecu_info.get('ecu_type', 'Unknown')
        self.info_labels['Bootloader'].text = str(ecu_info.get('in_bootloader', False))
        
        self.status_label.text = 'Connected successfully!'
        self.status_label.color = (0, 1, 0, 1)
        
    def show_error(self, message):
        """Show error message."""
        self.status_label.text = message
        self.status_label.color = (1, 0.27, 0.27, 1)


class FlashScreen(Screen):
    """Flash screen for ECU flashing."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_file = None
        self.build_ui()
        
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='Flash ECU',
            size_hint_y=0.08,
            font_size='20sp',
            bold=True
        )
        layout.add_widget(header)
        
        # File selection
        file_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        self.file_label = Label(
            text='No file selected',
            size_hint_x=0.6
        )
        file_layout.add_widget(self.file_label)
        
        select_btn = Button(
            text='Select File',
            size_hint_x=0.4,
            background_color=(0, 0.47, 1, 1)
        )
        select_btn.bind(on_press=self.select_file)
        file_layout.add_widget(select_btn)
        
        layout.add_widget(file_layout)
        
        # Flash button
        self.flash_btn = Button(
            text='Flash ECU',
            size_hint_y=0.1,
            background_color=(0, 0.47, 1, 1),
            disabled=True
        )
        self.flash_btn.bind(on_press=self.on_flash)
        layout.add_widget(self.flash_btn)
        
        # Progress bar
        self.progress_bar = ProgressBar(max=100, size_hint_y=0.05)
        layout.add_widget(self.progress_bar)
        
        # Status label
        self.status_label = Label(
            text='',
            size_hint_y=0.05,
            color=(1, 0.27, 0.27, 1)
        )
        layout.add_widget(self.status_label)
        
        # Matching tunes section
        tunes_label = Label(
            text='Matching Tunes',
            size_hint_y=0.05,
            font_size='16sp',
            bold=True
        )
        layout.add_widget(tunes_label)
        
        # Scrollable tune list
        scroll = ScrollView(size_hint_y=0.47)
        self.tune_list = Label(
            text='Connect to ECU to see matching tunes',
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.tune_list.bind(texture_size=self.tune_list.setter('size'))
        scroll.add_widget(self.tune_list)
        layout.add_widget(scroll)
        
        # Back button
        back_btn = Button(
            text='Back',
            size_hint_y=0.1,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
    def select_file(self, instance):
        """Open file chooser."""
        content = BoxLayout(orientation='vertical')
        
        filechooser = FileChooserListView(
            filters=['*.bin'],
            path='/sdcard' if platform == 'android' else os.path.expanduser('~')
        )
        content.add_widget(filechooser)
        
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        select_btn = Button(text='Select')
        cancel_btn = Button(text='Cancel')
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Select .bin File',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def on_select(instance):
            if filechooser.selection:
                self.selected_file = filechooser.selection[0]
                self.file_label.text = os.path.basename(self.selected_file)
                self.flash_btn.disabled = False
            popup.dismiss()
            
        select_btn.bind(on_press=on_select)
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
        
    def on_flash(self, instance):
        """Handle flash button press."""
        app = App.get_running_app()
        
        if not app.flasher or not app.flasher.connected:
            self.show_error('Please connect to ECU first')
            return
            
        if not self.selected_file:
            self.show_error('Please select a .bin file')
            return
            
        # Show warning popup
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(
            text='WARNING: Ensure your vehicle battery is fully charged or connected to a 12V+ charger. Power loss during flashing can damage the ECU.',
            text_size=(300, None)
        ))
        
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        yes_btn = Button(text='Proceed', background_color=(1, 0, 0, 1))
        no_btn = Button(text='Cancel')
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Battery Warning',
            content=content,
            size_hint=(0.9, 0.5)
        )
        
        def proceed(instance):
            popup.dismiss()
            self.start_flash()
            
        yes_btn.bind(on_press=proceed)
        no_btn.bind(on_press=popup.dismiss)
        
        popup.open()
        
    def start_flash(self):
        """Start flashing process."""
        self.flash_btn.disabled = True
        self.status_label.text = 'Flashing... Do not disconnect!'
        self.status_label.color = (1, 0.65, 0, 1)
        self.progress_bar.value = 0
        
        # Run flash in background thread
        threading.Thread(target=self.flash_thread, daemon=True).start()
        
    def flash_thread(self):
        """Background thread for flashing."""
        try:
            app = App.get_running_app()
            
            def progress_callback(percent):
                Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', percent), 0)
                
            app.flasher.flash_ecu(self.selected_file, progress_callback)
            
            Clock.schedule_once(lambda dt: self.flash_complete(), 0)
            
        except Exception as e:
            logger.error(f"Flash error: {e}")
            Clock.schedule_once(lambda dt: self.show_error(f'Flash failed: {str(e)}'), 0)
            
        finally:
            Clock.schedule_once(lambda dt: setattr(self.flash_btn, 'disabled', False), 0)
            
    def flash_complete(self):
        """Handle flash completion."""
        self.status_label.text = 'Flash completed successfully!'
        self.status_label.color = (0, 1, 0, 1)
        self.progress_bar.value = 100
        
    def show_error(self, message):
        """Show error message."""
        self.status_label.text = message
        self.status_label.color = (1, 0.27, 0.27, 1)


class DTCScreen(Screen):
    """DTC screen for reading and clearing codes."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='Diagnostic Trouble Codes',
            size_hint_y=0.08,
            font_size='20sp',
            bold=True
        )
        layout.add_widget(header)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        read_btn = Button(
            text='Read DTCs',
            background_color=(0, 0.47, 1, 1)
        )
        read_btn.bind(on_press=self.read_dtcs)
        btn_layout.add_widget(read_btn)
        
        clear_btn = Button(
            text='Clear DTCs',
            background_color=(1, 0.27, 0.27, 1)
        )
        clear_btn.bind(on_press=self.clear_dtcs)
        btn_layout.add_widget(clear_btn)
        
        layout.add_widget(btn_layout)
        
        # DTC list
        scroll = ScrollView(size_hint_y=0.72)
        self.dtc_label = Label(
            text='Press "Read DTCs" to scan for codes',
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.dtc_label.bind(texture_size=self.dtc_label.setter('size'))
        scroll.add_widget(self.dtc_label)
        layout.add_widget(scroll)
        
        # Back button
        back_btn = Button(
            text='Back',
            size_hint_y=0.1,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
    def read_dtcs(self, instance):
        """Read DTCs from ECU."""
        app = App.get_running_app()
        
        if not app.flasher or not app.flasher.connected:
            self.dtc_label.text = 'Error: Not connected to ECU'
            return
            
        self.dtc_label.text = 'Reading DTCs...'
        
        # Run in background thread
        threading.Thread(target=self.read_dtcs_thread, daemon=True).start()
        
    def read_dtcs_thread(self):
        """Background thread for reading DTCs."""
        try:
            app = App.get_running_app()
            dtcs = app.flasher.read_dtcs()
            
            if not dtcs:
                Clock.schedule_once(lambda dt: setattr(self.dtc_label, 'text', 'No DTCs found'), 0)
            else:
                dtc_text = '\n'.join([f"{dtc['text']} - Status: {bin(dtc['status'])[2:].zfill(8)}" for dtc in dtcs])
                Clock.schedule_once(lambda dt: setattr(self.dtc_label, 'text', dtc_text), 0)
                
        except Exception as e:
            logger.error(f"Read DTC error: {e}")
            Clock.schedule_once(lambda dt: setattr(self.dtc_label, 'text', f'Error: {str(e)}'), 0)
            
    def clear_dtcs(self, instance):
        """Clear DTCs from ECU."""
        app = App.get_running_app()
        
        if not app.flasher or not app.flasher.connected:
            self.dtc_label.text = 'Error: Not connected to ECU'
            return
            
        self.dtc_label.text = 'Clearing DTCs...'
        
        # Run in background thread
        threading.Thread(target=self.clear_dtcs_thread, daemon=True).start()
        
    def clear_dtcs_thread(self):
        """Background thread for clearing DTCs."""
        try:
            app = App.get_running_app()
            if app.flasher.clear_dtcs():
                Clock.schedule_once(lambda dt: setattr(self.dtc_label, 'text', 'DTCs cleared successfully'), 0)
            else:
                Clock.schedule_once(lambda dt: setattr(self.dtc_label, 'text', 'Failed to clear DTCs'), 0)
                
        except Exception as e:
            logger.error(f"Clear DTC error: {e}")
            Clock.schedule_once(lambda dt: setattr(self.dtc_label, 'text', f'Error: {str(e)}'), 0)


class SettingsScreen(Screen):
    """Settings screen for backup and reset."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='Settings',
            size_hint_y=0.1,
            font_size='20sp',
            bold=True
        )
        layout.add_widget(header)
        
        # Backup button
        backup_btn = Button(
            text='Backup ECU',
            size_hint_y=0.15,
            background_color=(0, 0.47, 1, 1)
        )
        backup_btn.bind(on_press=self.backup_ecu)
        layout.add_widget(backup_btn)
        
        # Reset button
        reset_btn = Button(
            text='Reset ECU',
            size_hint_y=0.15,
            background_color=(1, 0.27, 0.27, 1)
        )
        reset_btn.bind(on_press=self.reset_ecu)
        layout.add_widget(reset_btn)
        
        # Progress bar
        self.progress_bar = ProgressBar(max=100, size_hint_y=0.05)
        layout.add_widget(self.progress_bar)
        
        # Status label
        self.status_label = Label(
            text='',
            size_hint_y=0.45,
            color=(0, 1, 0, 1)
        )
        layout.add_widget(self.status_label)
        
        # Back button
        back_btn = Button(
            text='Back',
            size_hint_y=0.1,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
    def backup_ecu(self, instance):
        """Backup ECU."""
        app = App.get_running_app()
        
        if not app.flasher or not app.flasher.connected:
            self.status_label.text = 'Error: Not connected to ECU'
            self.status_label.color = (1, 0.27, 0.27, 1)
            return
            
        self.status_label.text = 'Starting backup...'
        self.status_label.color = (1, 0.65, 0, 1)
        self.progress_bar.value = 0
        
        # Run in background thread
        threading.Thread(target=self.backup_thread, daemon=True).start()
        
    def backup_thread(self):
        """Background thread for backup."""
        try:
            app = App.get_running_app()
            
            def progress_callback(percent):
                Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', percent), 0)
                
            # Save to Downloads folder on Android
            backup_dir = '/sdcard/Download' if platform == 'android' else os.path.expanduser('~/Downloads')
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_file = app.flasher.backup_ecu(None, progress_callback)
            
            Clock.schedule_once(lambda dt: self.backup_complete(backup_file), 0)
            
        except Exception as e:
            logger.error(f"Backup error: {e}")
            Clock.schedule_once(lambda dt: self.show_error(f'Backup failed: {str(e)}'), 0)
            
    def backup_complete(self, backup_file):
        """Handle backup completion."""
        self.status_label.text = f'Backup saved to:\n{backup_file}'
        self.status_label.color = (0, 1, 0, 1)
        self.progress_bar.value = 100
        
    def reset_ecu(self, instance):
        """Reset ECU."""
        app = App.get_running_app()
        
        if not app.flasher or not app.flasher.connected:
            self.status_label.text = 'Error: Not connected to ECU'
            self.status_label.color = (1, 0.27, 0.27, 1)
            return
            
        # Show confirmation popup
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='Are you sure you want to reset the ECU?'))
        
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        yes_btn = Button(text='Yes', background_color=(1, 0, 0, 1))
        no_btn = Button(text='No')
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Confirm Reset',
            content=content,
            size_hint=(0.8, 0.4)
        )
        
        def do_reset(instance):
            popup.dismiss()
            try:
                if app.flasher.reset_ecu():
                    self.status_label.text = 'ECU reset command sent'
                    self.status_label.color = (0, 1, 0, 1)
                else:
                    self.status_label.text = 'Failed to reset ECU'
                    self.status_label.color = (1, 0.27, 0.27, 1)
            except Exception as e:
                self.status_label.text = f'Error: {str(e)}'
                self.status_label.color = (1, 0.27, 0.27, 1)
                
        yes_btn.bind(on_press=do_reset)
        no_btn.bind(on_press=popup.dismiss)
        
        popup.open()
        
    def show_error(self, message):
        """Show error message."""
        self.status_label.text = message
        self.status_label.color = (1, 0.27, 0.27, 1)


class RFTXApp(App):
    """Main RFTX application."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flasher = None
        self.tune_matcher = None
        self.permissions_granted = False
        
    def build(self):
        """Build the app UI."""
        if platform == 'android':
            def on_permissions(granted):
                self.permissions_granted = granted
                if not granted:
                    logger.warning("Permissions not fully granted")
                    self.show_permissions_dialog()
                else:
                    logger.info("All permissions granted")
                    
            request_permissions_on_start(on_permissions)
            
        sm = ScreenManager()
        
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(FlashScreen(name='flash'))
        sm.add_widget(DTCScreen(name='dtc'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm
        
    def show_permissions_dialog(self):
        """Show dialog for missing permissions."""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(
            text='RFTX Tuning requires storage and USB permissions to function properly. Please grant permissions in settings.',
            text_size=(300, None)
        ))
        
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        settings_btn = Button(text='Open Settings', background_color=(0, 0.47, 1, 1))
        close_btn = Button(text='Close')
        btn_layout.add_widget(settings_btn)
        btn_layout.add_widget(close_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Permissions Required',
            content=content,
            size_hint=(0.9, 0.5),
            auto_dismiss=False
        )
        
        def open_settings(instance):
            permissions_manager.open_app_settings()
            popup.dismiss()
            
        settings_btn.bind(on_press=open_settings)
        close_btn.bind(on_press=popup.dismiss)
        
        popup.open()
        
    def on_stop(self):
        """Clean up on app exit."""
        if self.flasher:
            self.flasher.disconnect()
        if self.tune_matcher:
            self.tune_matcher.cleanup()


if __name__ == '__main__':
    RFTXApp().run()

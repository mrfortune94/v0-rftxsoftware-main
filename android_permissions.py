"""
Android Permissions Handler
Manages runtime permissions for Android devices.
"""

import logging
from kivy.utils import platform

logger = logging.getLogger('RFTX.Permissions')

if platform == 'android':
    from android.permissions import request_permissions, check_permission, Permission
    from jnius import autoclass
    
    # Android classes
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Settings = autoclass('android.provider.Settings')
    Uri = autoclass('android.net.Uri')
    Build = autoclass('android.os.Build')


class PermissionsManager:
    """Manage Android runtime permissions."""
    
    def __init__(self):
        """Initialize permissions manager."""
        self.permissions_granted = {}
        
    def request_storage_permissions(self, callback=None):
        """Request storage permissions."""
        if platform != 'android':
            if callback:
                callback(True)
            return True
            
        try:
            # Check Android version
            sdk_version = Build.VERSION.SDK_INT
            
            if sdk_version >= 30:
                # Android 11+ requires MANAGE_EXTERNAL_STORAGE
                logger.info("Requesting storage permissions for Android 11+")
                self._request_manage_storage(callback)
            else:
                # Android 10 and below
                logger.info("Requesting storage permissions for Android 10-")
                permissions = [
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE
                ]
                
                def permission_callback(permissions, grant_results):
                    granted = all(grant_results)
                    self.permissions_granted['storage'] = granted
                    logger.info(f"Storage permissions: {'granted' if granted else 'denied'}")
                    if callback:
                        callback(granted)
                        
                request_permissions(permissions, permission_callback)
                
        except Exception as e:
            logger.error(f"Error requesting storage permissions: {e}")
            if callback:
                callback(False)
            return False
            
    def _request_manage_storage(self, callback=None):
        """Request MANAGE_EXTERNAL_STORAGE permission (Android 11+)."""
        try:
            activity = PythonActivity.mActivity
            
            # Check if already granted
            if self._has_manage_storage_permission():
                logger.info("MANAGE_EXTERNAL_STORAGE already granted")
                self.permissions_granted['storage'] = True
                if callback:
                    callback(True)
                return
                
            # Open settings to grant permission
            intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
            uri = Uri.parse(f"package:{activity.getPackageName()}")
            intent.setData(uri)
            activity.startActivity(intent)
            
            # Note: This is asynchronous, user must manually grant permission
            logger.info("Opened settings for MANAGE_EXTERNAL_STORAGE permission")
            
            # Check permission after delay
            from kivy.clock import Clock
            def check_delayed(dt):
                granted = self._has_manage_storage_permission()
                self.permissions_granted['storage'] = granted
                if callback:
                    callback(granted)
                    
            Clock.schedule_once(check_delayed, 3.0)
            
        except Exception as e:
            logger.error(f"Error requesting MANAGE_EXTERNAL_STORAGE: {e}")
            if callback:
                callback(False)
                
    def _has_manage_storage_permission(self):
        """Check if MANAGE_EXTERNAL_STORAGE is granted."""
        try:
            Environment = autoclass('android.os.Environment')
            return Environment.isExternalStorageManager()
        except:
            return False
            
    def check_storage_permissions(self):
        """Check if storage permissions are granted."""
        if platform != 'android':
            return True
            
        try:
            sdk_version = Build.VERSION.SDK_INT
            
            if sdk_version >= 30:
                return self._has_manage_storage_permission()
            else:
                read_granted = check_permission(Permission.READ_EXTERNAL_STORAGE)
                write_granted = check_permission(Permission.WRITE_EXTERNAL_STORAGE)
                return read_granted and write_granted
                
        except Exception as e:
            logger.error(f"Error checking storage permissions: {e}")
            return False
            
    def request_usb_permissions(self, device, callback=None):
        """Request USB device permissions."""
        if platform != 'android':
            if callback:
                callback(True)
            return True
            
        try:
            from android_usb_serial import request_usb_permission
            
            granted = request_usb_permission(device)
            self.permissions_granted['usb'] = granted
            
            logger.info(f"USB permissions: {'granted' if granted else 'denied'}")
            
            if callback:
                callback(granted)
                
            return granted
            
        except Exception as e:
            logger.error(f"Error requesting USB permissions: {e}")
            if callback:
                callback(False)
            return False
            
    def request_all_permissions(self, callback=None):
        """Request all required permissions."""
        if platform != 'android':
            if callback:
                callback(True)
            return True
            
        logger.info("Requesting all permissions")
        
        # Request storage first
        def on_storage_granted(granted):
            if not granted:
                logger.warning("Storage permissions denied")
                if callback:
                    callback(False)
                return
                
            logger.info("All permissions granted")
            if callback:
                callback(True)
                
        self.request_storage_permissions(on_storage_granted)
        
    def open_app_settings(self):
        """Open app settings page."""
        if platform != 'android':
            return
            
        try:
            activity = PythonActivity.mActivity
            intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
            uri = Uri.parse(f"package:{activity.getPackageName()}")
            intent.setData(uri)
            activity.startActivity(intent)
            logger.info("Opened app settings")
        except Exception as e:
            logger.error(f"Error opening app settings: {e}")
            
    def get_permissions_status(self):
        """Get status of all permissions."""
        status = {
            'storage': self.check_storage_permissions(),
            'usb': self.permissions_granted.get('usb', False)
        }
        return status


# Global permissions manager instance
permissions_manager = PermissionsManager()


def request_permissions_on_start(callback=None):
    """Request permissions when app starts."""
    if platform == 'android':
        logger.info("Requesting permissions on app start")
        permissions_manager.request_all_permissions(callback)
    else:
        if callback:
            callback(True)


[app]

title = WebMonitorApp
package.name = WebMonitorApp
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 2.0

requirements = python3,kivy,plyer

orientation = portrait

android.permissions = INTERNET,FOREGROUND_SERVICE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.service = service.py

fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1

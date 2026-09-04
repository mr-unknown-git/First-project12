# filename="buildozer.spec"

[app]

title = TikTok View Bot
package.name = tiktokviewbot
package.domain = org.tiktokviewbot
source.dir = .

source.include_exts = py,png,jpg,kv,atlas
requirements = python3,kivy,httpx
requirements.source = kivy

version = 1.0

orientation = portrait

# Architecture: Use arm64-v8a for modern Android phones
android.arch = arm64-v8a

# API Level 33 is currently the standard stable version
android.api = 33
android.minapi = 21

# NDK 25b is the latest stable release
android.ndk = 25b

# CRITICAL FIX: Pin build tools to a specific old version to bypass license errors
android.build-tools = 33.0.0

# CRITICAL FIX: Automatically accept all licenses without prompting
android.acceptlicenses = 1

android.private_storage = True

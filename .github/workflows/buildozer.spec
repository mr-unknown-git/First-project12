# filename="buildozer.spec"
[app]

title = TikTok View Bot
package.name = tiktokviewbot
package.domain = org.tiktokviewbot
source.dir = .

source.include_exts = py,png,jpg,kv,atlas
requirements = python3,kivy,httpx

version = 1.0

orientation = portrait

android.arch = armeabi-v7a
android.api = 30
android.minapi = 21
android.sdk = 24
android.ndk = 23b

android.private_storage = True

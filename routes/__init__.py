# --- محتويات ملف __init__.py (مثال) ---

from flask import Flask
# (قد تحتاجين لاستيراد db و login_manager هنا أيضاً)

def create_app():
    app = Flask(__name__)
    # ... إعدادات التطبيق (مثل app.config...) ...
    
    # 1. استيراد البلوبرينت (تأكدي أن المسار صحيح)
    from .friend_routes import friend_bp
    # (استيراد باقي الـ Blueprints الأخرى أيضاً: auth_routes, user_routes, etc.)

    # 2. تسجيل البلوبرينت (الخطوة الحاسمة)
    app.register_blueprint(friend_bp)
    # (تسجيل باقي الـ Blueprints)
    
    return app

# إذا كنتِ تستخدمين app.py بدلاً من Factory:
# app = Flask(__name__)
# from .friend_routes import friend_bp
# app.register_blueprint(friend_bp)

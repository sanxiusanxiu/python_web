"""
作为你的项目的运行在 ASGI 兼容的 Web 服务器上的入口

ASGI config for vote_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vote_site.settings')

application = get_asgi_application()

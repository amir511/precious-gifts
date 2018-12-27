from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

@apphook_pool.register
class StoreApp(CMSApp):
    name = 'store'
    app_name = 'store'
    urls = ['precious_gifts.apps.store.urls']



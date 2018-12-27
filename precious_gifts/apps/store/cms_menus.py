from django.core.urlresolvers import reverse
from cms.menu_bases import CMSAttachMenu
from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from precious_gifts.apps.store.models import Product, Cart, Order

class StoreMenu(CMSAttachMenu):
    name = 'Store Menu'

    def get_nodes(self, request):
        """
        This method is used to build the menu tree.
        """
        products_node = NavigationNode(title='Browse products', url=reverse('store:product_list'), id=1)
        cart_node = NavigationNode(title='My Cart', url=reverse('store:view_cart'), id=2)
        orders_node = NavigationNode(title='My Orders', url=reverse('store:order_list'), id=3)

        return [products_node, cart_node, orders_node]

menu_pool.register_menu(StoreMenu)
## Shop
This handles the creation of shops, along with the items that specific shops have. This is where a new shop should be created or current shops altered.

- [Transaction Logic](#transaction-logic)
- [Shop Stock](#shop-stock)

### Transaction Logic
`shop.py` contains the logic for interacting with shops. This involves: 
- Checking if the player has enough money to buy a chosen item
- Retrieving the cost of items
- Buying items
- Selling items

These are all functions belonging to the super-class `Shop` from which all shops should inherit, thus providing them with the same functionality.

### Shop Stock 
Each shop has its own inventory, held in `self.shop_inv`. This is a list of up to 25 items, holding the names of items, how many are in stock and an item type, either weapon, potion or throwable. This means that `ui.py` can retrieve the name, and thus render the sprites when creating the shop. 

An item can be added to a shop through:
```python
self.shop_inv[0] = ["knight_sword", self.max_stock, "weapon"]
```
Passing the item name, corresponding to those seen in `equimpent_list.py`. The indexing in `shop_inv[0]` corresponds to which slot the item should be in, and so the order and groupings of items can be customised.
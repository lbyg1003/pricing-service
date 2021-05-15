from models.alert import Alert

# everytime run the alert_updater, will load the item's current price from item URL,
# and compare with the saved alert price
alerts = Alert.all()

for alert in alerts:
    alert.load_item_price()
    alert.notify_if_price_reached()

if not alerts:
    print("No alert has been created. Add an item and a price limit to begin.")

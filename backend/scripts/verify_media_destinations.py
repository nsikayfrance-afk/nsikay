from media_library.models import MediaDestination

total = MediaDestination.objects.count()
internal = MediaDestination.objects.filter(
    destination_type="INTERNAL"
).count()
external = MediaDestination.objects.filter(
    destination_type="EXTERNAL"
).count()

print()
print("TOTAL =", total)
print("INTERNES =", internal)
print("EXTERNES =", external)

print()
print("===== DESTINATIONS =====")

for destination in MediaDestination.objects.order_by("id"):
    print(
        destination.id,
        "|",
        destination.destination_type,
        "|",
        destination.channel_type,
        "|",
        destination.code,
        "|",
        destination.name,
        "| ACTIVE =",
        destination.active,
    )
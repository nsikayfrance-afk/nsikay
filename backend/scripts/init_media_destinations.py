from media_library.models import MediaDestination

DESTINATIONS = [
    ("nsikay_tv", "NSIKAY TV", "INTERNAL", "NSIKAY_TV"),
    ("economie", "Économie", "INTERNAL", "ECONOMIE"),
    ("sport", "Sport & Loisirs", "INTERNAL", "SPORT"),
    ("culture", "Culture & Art", "INTERNAL", "CULTURE"),
    ("technologie", "Technologie & Innovation", "INTERNAL", "TECHNOLOGIE"),
    ("agriculture", "Agriculture & Agronomie", "INTERNAL", "AGRICULTURE"),
    ("environnement", "Environnement", "INTERNAL", "ENVIRONNEMENT"),
    ("social", "Social", "INTERNAL", "SOCIAL"),
    ("religion_histoire", "Religion & Histoire", "INTERNAL", "RELIGION"),
    ("adult", "+18", "INTERNAL", "ADULT"),
    ("evenements", "Événements", "INTERNAL", "EVENEMENTS"),
    ("publicite", "Publicité", "INTERNAL", "PUBLICITE"),
    ("youtube", "YouTube", "EXTERNAL", "YOUTUBE"),
    ("facebook", "Facebook", "EXTERNAL", "FACEBOOK"),
    ("instagram", "Instagram", "EXTERNAL", "INSTAGRAM"),
    ("tiktok", "TikTok", "EXTERNAL", "TIKTOK"),
    ("twitch", "Twitch", "EXTERNAL", "TWITCH"),
    ("linkedin", "LinkedIn", "EXTERNAL", "LINKEDIN"),
    ("rtmp_custom", "RTMP personnalisé", "EXTERNAL", "RTMP"),
    ("srt_custom", "SRT personnalisé", "EXTERNAL", "SRT"),
    ("hls_custom", "HLS personnalisé", "EXTERNAL", "HLS"),
]

created = 0
updated = 0

for code, name, destination_type, channel_type in DESTINATIONS:
    obj, was_created = MediaDestination.objects.get_or_create(
        code=code,
        defaults={
            "name": name,
            "destination_type": destination_type,
            "channel_type": channel_type,
            "active": True,
        },
    )

    if was_created:
        created += 1
    else:
        changed = False

        if obj.name != name:
            obj.name = name
            changed = True

        if obj.destination_type != destination_type:
            obj.destination_type = destination_type
            changed = True

        if obj.channel_type != channel_type:
            obj.channel_type = channel_type
            changed = True

        if not obj.active:
            obj.active = True
            changed = True

        if changed:
            obj.save()
            updated += 1

print()
print("Destinations créées :", created)
print("Destinations mises à jour :", updated)
print("Total destinations :", MediaDestination.objects.count())

print()
print("===== INTERNES =====")
for obj in MediaDestination.objects.filter(
    destination_type="INTERNAL"
).order_by("id"):
    print(obj.id, "|", obj.code, "|", obj.name, "|", obj.channel_type)

print()
print("===== EXTERNES =====")
for obj in MediaDestination.objects.filter(
    destination_type="EXTERNAL"
).order_by("id"):
    print(obj.id, "|", obj.code, "|", obj.name, "|", obj.channel_type)

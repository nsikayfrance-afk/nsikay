from pathlib import Path

file = Path("dashboard/urls.py")

content = file.read_text(encoding="utf-8")

route = '''
    path("stats/", views.dashboard_stats),
'''

if 'path("stats/"' not in content:
    content = content.replace(
        'urlpatterns = [',
        'urlpatterns = [\n' + route
    )

file.write_text(content, encoding="utf-8")

print("=== ROUTE STATS DASHBOARD AJOUTEE ===")


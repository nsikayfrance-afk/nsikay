from django.db import migrations


def convert_currency(apps, schema_editor):
    WenzeProduct = apps.get_model("wenze", "WenzeProduct")
    WenzeOrder = apps.get_model("wenze", "WenzeOrder")
    Currency = apps.get_model("finance", "Currency")

    # Les devises peuvent ne pas encore exister dans une base
    # nouvellement créée par Django pour les tests.
    #
    # Si EUR existe, on conserve la conversion historique des
    # anciennes valeurs texte "EUR".
    # Si EUR n'existe pas encore, la migration ne doit pas bloquer
    # la création de la base.

    eur = Currency.objects.filter(code="EUR").first()

    if eur is None:
        return

    # Anciennes valeurs texte EUR
    WenzeProduct.objects.filter(currency="EUR").update(currency=eur.id)
    WenzeOrder.objects.filter(currency="EUR").update(currency=eur.id)


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0008_alter_marketplacecommission_rate"),
        ("wenze", "0002_wenzeorder_paid_at_wenzeorder_payment_fee_and_more"),
    ]

    operations = [
        migrations.RunPython(
            convert_currency,
            migrations.RunPython.noop,
        ),
    ]

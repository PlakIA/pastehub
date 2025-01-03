# Generated by Django 4.2.17 on 2024-12-16 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("paste", "0002_alter_pasteversion_paste"),
    ]

    operations = [
        migrations.AddField(
            model_name="paste",
            name="language",
            field=models.CharField(
                choices=[
                    ("markup", "Markup"),
                    ("css", "CSS"),
                    ("clike", "C-like"),
                    ("javascript", "JavaScript"),
                    ("python", "Python"),
                    ("java", "Java"),
                    ("csharp", "C#"),
                    ("cpp", "C++"),
                    ("php", "PHP"),
                    ("ruby", "Ruby"),
                    ("swift", "Swift"),
                    ("go", "Go"),
                    ("bash", "Bash"),
                    ("sql", "SQL"),
                    ("html", "HTML"),
                    ("xml", "XML"),
                    ("json", "JSON"),
                    ("yaml", "YAML"),
                    ("typescript", "TypeScript"),
                    ("rust", "Rust"),
                    ("kotlin", "Kotlin"),
                    ("dart", "Dart"),
                    ("scala", "Scala"),
                    ("shell", "Shell"),
                    ("powershell", "PowerShell"),
                    ("haskell", "Haskell"),
                    ("elixir", "Elixir"),
                    ("text", "Plain Text"),
                ],
                default="text",
                help_text="Выберите язык для подсветки",
                max_length=50,
                verbose_name="язык для подсветки",
            ),
        ),
        migrations.AddField(
            model_name="protectedpaste",
            name="language",
            field=models.CharField(
                choices=[
                    ("markup", "Markup"),
                    ("css", "CSS"),
                    ("clike", "C-like"),
                    ("javascript", "JavaScript"),
                    ("python", "Python"),
                    ("java", "Java"),
                    ("csharp", "C#"),
                    ("cpp", "C++"),
                    ("php", "PHP"),
                    ("ruby", "Ruby"),
                    ("swift", "Swift"),
                    ("go", "Go"),
                    ("bash", "Bash"),
                    ("sql", "SQL"),
                    ("html", "HTML"),
                    ("xml", "XML"),
                    ("json", "JSON"),
                    ("yaml", "YAML"),
                    ("typescript", "TypeScript"),
                    ("rust", "Rust"),
                    ("kotlin", "Kotlin"),
                    ("dart", "Dart"),
                    ("scala", "Scala"),
                    ("shell", "Shell"),
                    ("powershell", "PowerShell"),
                    ("haskell", "Haskell"),
                    ("elixir", "Elixir"),
                    ("text", "Plain Text"),
                ],
                default="text",
                help_text="Выберите язык для подсветки",
                max_length=50,
                verbose_name="язык для подсветки",
            ),
        ),
    ]

import json
from django.core.management.base import BaseCommand
from Horrorify.models import Story

class Command(BaseCommand):
    help = "Add scraped stories to the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file",
            type=str,
            help="The JSON file containing stories to be imported",
        )

    def handle(self, *args, **kwargs):
        json_file_path = kwargs["json_file"]

        try:
            with open(json_file_path, "r") as json_file:
                stories = json.load(json_file)
                for story_data in stories:
                    story, created = Story.objects.get_or_create(
                        title=story_data["title"],
                        defaults={
                            'author_name': story_data["Author"],
                            'author_link': story_data["AuthorLink"],
                            'content': story_data["content"],
                            'is_scraped': True,  # Set is_scraped to True when the story is created
                        }
                    )
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f"Successfully added story: {story.title}")
                        )
                    else:
                        # If the story already exists, update the is_scraped field to True
                        if not story.is_scraped:
                            story.is_scraped = True
                            story.save()
                            self.stdout.write(
                                self.style.SUCCESS(f"Updated story as scraped: {story.title}")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"Story already exists and is already marked as scraped: {story.title}")
                            )
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File "{json_file_path}" not found'))
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("Failed to decode JSON file"))

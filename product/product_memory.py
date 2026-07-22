import os
import json

class ProductMemory:
    def __init__(self, base_dir="product/memory"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.requirements_file = os.path.join(self.base_dir, "requirements.json")
        self.epics_file = os.path.join(self.base_dir, "epics.json")
        self.roadmaps_file = os.path.join(self.base_dir, "roadmaps.json")
        self.releases_file = os.path.join(self.base_dir, "releases.json")

    def save_requirement(self, requirement):
        pass

    def save_epic(self, epic):
        pass

    def save_story(self, story):
        pass

    def save_roadmap(self, roadmap):
        pass

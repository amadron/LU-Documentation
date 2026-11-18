import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
from search_index import compact_documents


class SearchIndexTests(unittest.TestCase):
    def test_detail_names_ids_and_descriptions_remain_searchable(self):
        documents = [
            {"location": "wiki/items/10021/", "title": "Un-Stink Potion", "text": "LOT: 10021"},
            {"location": "wiki/items/10021/#description", "title": "Description", "text": "Double-click to use!"},
            {"location": "wiki/items/10021/#drops", "title": "Drops", "text": "Large table"},
            {"location": "wiki/quests/319/", "title": "Finish Line - Quest 319", "text": "Definition ID: 319"},
            {"location": "wiki/quests/319/#rewards", "title": "Rewards", "text": "Large table"},
            {"location": "wiki/npcs/14381/", "title": "Maelstrom Spider Queen", "text": "LOT 14381"},
            {"location": "wiki/npcs/14381/#mapped-placements", "title": "Mapped placements", "text": "Large table"},
            {"location": "wiki/pets/3050/#history", "title": "Elephant", "text": "LOT 3050"},
            {"location": "wiki/Getting%20Started/#movement", "title": "Movement", "text": "Player guide"},
        ]
        result = compact_documents(documents)
        self.assertEqual(result, [documents[i] for i in (0, 1, 3, 5, 7, 8)])

    def test_catalog_titles_remain_without_large_tables(self):
        documents = [
            {"location": "wiki/items/sources/matrix-414/", "title": "Loot matrix 414", "text": "Large table"},
            {"location": "wiki/items/sources/matrix-414/#items", "title": "Items", "text": "Large table"},
            {"location": "wiki/quests/indexes/npcs/", "title": "NPCs", "text": "Large table"},
            {"location": "wiki/npcs/indexes/enemies-1/", "title": "Enemies", "text": "Large table"},
            {"location": "wiki/items/", "title": "Item database", "text": "Landing page"},
        ]
        result = compact_documents(documents)
        self.assertEqual(result, [
            {**documents[0], "text": ""},
            {**documents[2], "text": ""},
            {**documents[3], "text": ""},
            documents[4],
        ])
        self.assertEqual(documents[0]["text"], "Large table")


if __name__ == "__main__":
    unittest.main()

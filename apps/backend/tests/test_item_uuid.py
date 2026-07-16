import sys
import unittest
from pathlib import Path
from uuid import UUID, uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from database.models.files import FileModel
from database.models.items import ItemModel


class ItemUuidTests(unittest.TestCase):
    def test_item_model_uses_uuid_primary_key(self):
        item_uuid = uuid4()
        item = ItemModel(
            uuid=item_uuid,
            owner_id=1,
            link_hash="abc123",
            title="Example",
            description="A test item",
        )

        self.assertEqual(item.uuid, item_uuid)
        self.assertIsInstance(item.uuid, UUID)

    def test_file_model_can_reference_item_uuid(self):
        item_uuid = uuid4()
        file_record = FileModel(
            uuid=uuid4(),
            creator_id=1,
            item_id=item_uuid,
            filename="example.png",
            content_type="image/png",
            size=10,
            storage_path="uploads/example.png",
        )

        self.assertEqual(file_record.item_id, item_uuid)


if __name__ == "__main__":
    unittest.main()

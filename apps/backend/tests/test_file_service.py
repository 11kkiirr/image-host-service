import asyncio
import io
import sys
import unittest
from pathlib import Path

from fastapi import UploadFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from database.models.files import FileModel
from services.file.service import FileService


class FakeFileRepository:
    def __init__(self):
        self.saved_files = []

    async def create_files(self, files):
        self.saved_files = list(files)
        return self.saved_files


class FakeUnitOfWork:
    def __init__(self):
        self.files = FakeFileRepository()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FileServiceTests(unittest.TestCase):
    def test_process_file_upload_creates_sqlalchemy_model(self):
        async def run_test():
            uow = FakeUnitOfWork()
            service = FileService(uow)
            upload = UploadFile(
                filename="example.png",
                file=io.BytesIO(b"fake-image-data"),
                headers={"content-type": "image/png"},
            )

            await service.process_file_upload(files=[upload], user_id=7, item_id=None)

            self.assertEqual(len(uow.files.saved_files), 1)
            saved = uow.files.saved_files[0]
            self.assertIsInstance(saved, FileModel)
            self.assertEqual(saved.creator_id, 7)
            self.assertEqual(saved.filename, "example.png")
            self.assertIsNone(saved.item_id)
            self.assertTrue(saved.uuid)
            self.assertTrue(saved.storage_path.startswith("uploads/"))

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()

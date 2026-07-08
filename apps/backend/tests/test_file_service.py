import asyncio
import io
import sys
import unittest
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.db.base.model import Base
from database.models.files import FileModel
from database.repositories.files import FileRepository
from database.schemas.files import FileReadSchema
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

    def test_repository_get_file_by_uuid_accepts_string_uuid(self):
        async def run_test():
            engine = create_async_engine("sqlite+aiosqlite:///:memory:")
            async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

            try:
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)

                async with async_session() as session:
                    file_record = FileModel(
                        uuid=uuid4(),
                        creator_id=1,
                        filename="example.png",
                        content_type="image/png",
                        size=10,
                        storage_path="uploads/example.png",
                    )
                    session.add(file_record)
                    await session.commit()

                    repository = FileRepository(session)
                    fetched = await repository.get_file_by_uuid(str(file_record.uuid))

                self.assertIsNotNone(fetched)
                self.assertEqual(fetched.uuid, file_record.uuid)
            finally:
                await engine.dispose()

        asyncio.run(run_test())

    def test_get_file_metadata_by_uuid_supports_uuid_primary_key(self):
        async def run_test():
            file_uuid = uuid4()
            file_record = FileModel(
                uuid=file_uuid,
                creator_id=1,
                filename="example.png",
                content_type="image/png",
                size=10,
                storage_path="uploads/example.png",
            )

            class FakeFileRepositoryWithRead:
                async def get_file_by_uuid(self, requested_uuid):
                    self.requested_uuid = requested_uuid
                    return file_record

            class FakeUnitOfWorkWithRead:
                def __init__(self, files_repo):
                    self.files = files_repo

                async def __aenter__(self):
                    return self

                async def __aexit__(self, exc_type, exc, tb):
                    return False

            repo = FakeFileRepositoryWithRead()
            uow = FakeUnitOfWorkWithRead(repo)
            service = FileService(uow)

            metadata = await service.get_file_metadata_by_uuid(str(file_uuid))

            self.assertIsInstance(metadata, FileReadSchema)
            self.assertEqual(metadata.uuid, file_uuid)
            self.assertEqual(metadata.filename, "example.png")
            self.assertEqual(metadata.storage_path, "uploads/example.png")

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()

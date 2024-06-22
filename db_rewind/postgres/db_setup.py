from db_rewind.postgres.os_handler.os_response_dto import OsResponseDTO
from db_rewind.postgres.procedures.archive_wal_files import ArchiveWalFiles
from db_rewind.postgres.procedures.base_procedure import BaseProcedure
from db_rewind.postgres.procedures.config_file_setup import ConfigFileSetup
from db_rewind.postgres.procedures.create_db_base_backup import CreateDBBaseBackup
from db_rewind.postgres.procedures.create_missing_directories import CreateMissingDirectories
from db_rewind.postgres.procedures.db_server_manager import DBServerManager


class DBSetup:
    @staticmethod
    def execute() -> OsResponseDTO:
        return DBSetup.get_procedures().execute()

    @staticmethod
    def get_procedures() -> BaseProcedure:
        return ConfigFileSetup().next(
            CreateMissingDirectories().next(
                DBServerManager.restart().next(
                    ArchiveWalFiles().next(
                        CreateDBBaseBackup()
                    )
                )
            )
        )

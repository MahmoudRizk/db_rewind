from vendors.postgres.os_handler.os_response_dto import OsResponseDTO
from vendors.postgres.procedures.archive_wal_files import ArchiveWalFiles
from vendors.postgres.procedures.base_procedure import BaseProcedure
from vendors.postgres.procedures.config_file_setup import ConfigFileSetup
from vendors.postgres.procedures.create_db_base_backup import CreateDBBaseBackup
from vendors.postgres.procedures.db_server_manager import DBServerManager


class DBSetup:
    @staticmethod
    def execute() -> OsResponseDTO:
        return DBSetup.get_procedures().execute()

    @staticmethod
    def get_procedures() -> BaseProcedure:
        return ConfigFileSetup().next(
            DBServerManager.restart().next(
                ArchiveWalFiles().next(
                    CreateDBBaseBackup()
                )
            )
        )

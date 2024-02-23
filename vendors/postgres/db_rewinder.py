from vendors.postgres.os_handler.os_response_dto import OsResponseDTO
from vendors.postgres.procedures.archive_wal_files import ArchiveWalFiles
from vendors.postgres.procedures.base_procedure import BaseProcedure
from vendors.postgres.procedures.create_recovery_signal_file import CreateRecoverySignalFile
from vendors.postgres.procedures.db_server_manager import DBServerManager
from vendors.postgres.procedures.destroy_db_data import DestroyDBData
from vendors.postgres.procedures.restore_db_base_backup import RestoreDBBaseBackup
from vendors.postgres.procedures.set_db_rewind_date import SetDBRewindDate


class DBRewinder:
    @staticmethod
    def execute() -> OsResponseDTO:
        return DBRewinder.get_procedures().execute()

    @staticmethod
    def get_procedures() -> BaseProcedure:
        return ArchiveWalFiles().next(
            DBServerManager(command='stop').next(
                DestroyDBData().next(
                    RestoreDBBaseBackup().next(
                        CreateRecoverySignalFile().next(
                            SetDBRewindDate().next(
                                DBServerManager(command='start')
                            )
                        )
                    )
                )
            )
        )

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
    def execute(db_rewind_date: str) -> OsResponseDTO:
        return DBRewinder.get_procedures(db_rewind_date=db_rewind_date).execute()

    @staticmethod
    def get_procedures(db_rewind_date: str) -> BaseProcedure:
        return ArchiveWalFiles().next(
            DBServerManager(command='stop').next(
                DestroyDBData().next(
                    RestoreDBBaseBackup().next(
                        CreateRecoverySignalFile().next(
                            SetDBRewindDate(db_rewind_date=db_rewind_date).next(
                                DBServerManager(command='start')
                            )
                        )
                    )
                )
            )
        )

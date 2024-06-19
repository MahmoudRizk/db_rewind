from db_rewind.postgres.os_handler.os_response_dto import OsResponseDTO
from db_rewind.postgres.procedures.archive_wal_files import ArchiveWalFiles
from db_rewind.postgres.procedures.base_procedure import BaseProcedure
from db_rewind.postgres.procedures.create_recovery_signal_file import CreateRecoverySignalFile
from db_rewind.postgres.procedures.db_server_manager import DBServerManager
from db_rewind.postgres.procedures.destroy_db_data import DestroyDBData
from db_rewind.postgres.procedures.remove_recovery_signal_file import RemoveRecoverySignalFile
from db_rewind.postgres.procedures.restore_db_base_backup import RestoreDBBaseBackup
from db_rewind.postgres.procedures.set_db_rewind_date import SetDBRewindDate


class DBRewinder:
    @staticmethod
    def execute() -> OsResponseDTO:
        return DBRewinder.get_procedures().execute()

    @staticmethod
    def get_procedures() -> BaseProcedure:
        return ArchiveWalFiles().next(
            DBServerManager.stop().next(
                DestroyDBData().next(
                    RestoreDBBaseBackup().next(
                        CreateRecoverySignalFile().next(
                            SetDBRewindDate().next(
                                DBServerManager.start().next(
                                    RemoveRecoverySignalFile().next(
                                        DBServerManager.restart()
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )

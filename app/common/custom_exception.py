import sys


class CustomException(Exception):
    def __init__(self, error_message: Exception, error_detail: sys):
        super().__init__(str(error_message))
        self.error_message = self._get_detailed_error(error_message, error_detail)

    @staticmethod
    def _get_detailed_error(error_message: Exception, error_detail: sys) -> str:
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        return (
            f"Error in [{file_name}] "
            f"at line [{line_number}]: "
            f"{str(error_message)}"
        )

    def __str__(self) -> str:
        return self.error_message

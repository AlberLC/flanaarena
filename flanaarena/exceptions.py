class UpdateDownloadError(Exception):
    def __init__(self) -> None:
        super().__init__('Update download failed')

class IncorrectFileType(Exception):
    message = 'Incorrect file type!'
    status = 415


class FileDoesntExists(Exception):
    message = "File doesn't exists!"
    status = 500

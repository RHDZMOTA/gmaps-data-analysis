from conf.settings import FilesConfig
import os


def create_dir(reference_path):
    if not os.path.exists(reference_path):
        os.mkdir(reference_path)


def create_dirs():
    create_dir(FilesConfig.Paths.data)
    create_dir(FilesConfig.Paths.raw_data)
    create_dir(FilesConfig.Paths.output)


if __name__ == "__main__":
    create_dirs()

import unicodedata
from pathlib import Path
from re import sub as re_sub

import yaml
from git import Repo, exc


class DTLRepo:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, args, repo_path, exception_handler):
        self.handle = exception_handler
        self.yaml_extensions = ["yaml", "yml"]
        self.url = args.url
        self.repo_path = repo_path
        self.branch = args.branch
        self.repo = None
        self.cwd = Path.cwd()

        if Path(self.repo_path).is_dir():
            self.pull_repo()
        else:
            self.clone_repo()

    def get_relative_path(self):
        return self.repo_path

    def get_absolute_path(self):
        return self.cwd / self.repo_path

    def get_devices_path(self):
        return self.get_absolute_path() / "device-types"

    def get_modules_path(self):
        return self.get_absolute_path() / "module-types"

    @staticmethod
    def slug_format(name):
        value = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
        value = re_sub(r"[^\w\s-]", "", value.lower())
        return re_sub(r"[-\s]+", "-", value).strip("-_")

    def pull_repo(self):
        try:
            self.handle.log(f"Package devicetype-library is already installed, updating {self.get_absolute_path()}")
            self.repo = Repo(self.repo_path)
            self.repo.remotes.origin.pull()
            self.repo.git.checkout(self.branch)
            self.handle.verbose_log(f"Pulled Repo {self.repo.remotes.origin.url}")
        except exc.GitCommandError as git_error:
            self.handle.exception("GitCommandError", self.repo.remotes.origin.url, git_error)
        except exc.GitError as git_error:
            self.handle.exception("Exception", "Git Repository Error", git_error)

    def clone_repo(self):
        try:
            self.repo = Repo.clone_from(self.url, self.get_absolute_path(), branch=self.branch)
            self.handle.log(f"Package Installed {self.repo.remotes.origin.url}")
        except exc.GitCommandError as git_error:
            self.handle.exception("GitCommandError", self.url, git_error)
        except exc.GitError as git_error:
            self.handle.exception("Exception", "Git Repository Error", git_error)

    def get_devices(self, base_path, vendors: list | None = None):
        files = []
        discovered_vendors = []
        base_path = Path(base_path)
        vendor_dirs = [p.name for p in base_path.iterdir() if p.is_dir()]

        for folder in [vendor for vendor in vendor_dirs if not vendors or vendor.casefold() in vendors]:
            if folder.casefold() != "testing":
                discovered_vendors.append({"name": folder, "slug": self.slug_format(folder)})
                for extension in self.yaml_extensions:
                    files.extend((base_path / folder).glob(f"*.{extension}"))
        return files, discovered_vendors

    def parse_files(self, files: list, slugs: list | None = None):
        device_types = []
        for file in files:
            with open(file, encoding="utf-8") as stream:
                try:
                    data = yaml.safe_load(stream)
                except yaml.YAMLError as excep:
                    self.handle.verbose_log(excep)
                    continue
                manufacturer = data["manufacturer"]
                data["manufacturer"] = {"name": manufacturer, "slug": self.slug_format(manufacturer)}

                # Save file location to resolve any relative paths for images
                data["src"] = str(file)

            if slugs:
                slug_present = any(s.casefold() in data.get("slug", "").casefold() for s in slugs)
                if not slug_present:
                    self.handle.verbose_log(f"Skipping {data['model']}")
                    continue

            device_types.append(data)
        return device_types

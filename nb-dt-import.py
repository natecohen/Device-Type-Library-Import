#!/usr/bin/env python3
import time

import settings
from netbox_api import NetBox


def main():
    start_time = time.perf_counter()
    args = settings.args

    netbox = NetBox(settings)
    files, vendors = settings.dtl_repo.get_devices(f"{settings.dtl_repo.repo_path}/device-types/", args.vendors)

    settings.handle.log(f"{len(vendors)} Vendors Found")
    device_types = settings.dtl_repo.parse_files(files, slugs=args.slugs)
    settings.handle.log(f"{len(device_types)} Device-Types Found")
    netbox.create_manufacturers(vendors)
    netbox.create_device_types(device_types, replace_existing_images=args.replace_existing_images)

    settings.handle.log("Modules Enabled. Creating Modules...")
    files, vendors = settings.dtl_repo.get_devices(f"{settings.dtl_repo.repo_path}/module-types/", args.vendors)
    settings.handle.log(f"{len(vendors)} Module Vendors Found")
    module_types = settings.dtl_repo.parse_files(files, slugs=args.slugs)
    normalized_modules = netbox.normalize_module_types(module_types)
    settings.handle.log(f"{len(module_types)} Module-Types Found")
    netbox.create_manufacturers(vendors)
    netbox.create_module_types(normalized_modules)

    settings.handle.log("Rack-Types Enabled. Creating Racks...")
    files, vendors = settings.dtl_repo.get_devices(f"{settings.dtl_repo.repo_path}/rack-types/", args.vendors)
    settings.handle.log(f"{len(vendors)} Rack Vendors Found")
    rack_types = settings.dtl_repo.parse_files(files, slugs=args.slugs)
    settings.handle.log(f"{len(rack_types)} Rack-Types Found")
    netbox.create_manufacturers(vendors)
    netbox.create_rack_types(rack_types)

    settings.handle.log("---")
    settings.handle.verbose_log(f"Script took {time.perf_counter() - start_time:.2f} seconds to run")
    settings.handle.log(f"{netbox.counter['added']} devices created")
    settings.handle.log(f"{netbox.counter['images']} images uploaded")
    settings.handle.log(f"{netbox.counter['updated']} interfaces/ports updated")
    settings.handle.log(f"{netbox.counter['manufacturer']} manufacturers created")
    settings.handle.log(f"{netbox.counter['module_added']} modules created")
    settings.handle.log(f"{netbox.counter['module_port_added']} module interface / ports created")
    settings.handle.log(f"{netbox.counter['rack_types_added']} rack-types created")


if __name__ == "__main__":
    main()

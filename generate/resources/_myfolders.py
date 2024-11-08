# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import deque
from cdktf_cdktf_provider_google.folder import Folder
import util


def bfs_navigate_folder(dictionary):
    add_folders = []
    queue = deque([("", "", dictionary)])
    new_folder_path = ""
    while queue:
        folder_parent, folder_name, current_folders = queue.popleft()
        if folder_name:
            new_folder_path = "/".join([folder_parent, folder_name])
            add_folders.append((folder_parent, new_folder_path, folder_name))
        # Enqueue child folders
        for node, sub_nodes in current_folders.items():
            queue.append((new_folder_path, node, sub_nodes))
    return add_folders


def create_folder(self, folder_path, new_folder_path, folder_name):
    if self.which_node(folder_path) == "folder":
        folder_parent = self.tf_ref("folder", folder_path)
    else:
        folder_parent = f'organizations/{self.tf_ref("organization", "/")}'

    self.created["folders"][new_folder_path] = Folder(
        self,
        f"fldr_{util.clean_tf_folder(new_folder_path)}",
        display_name=folder_name,
        parent=folder_parent,
    )


def generate_folders(self, my_resource, resource):
    add_folders = bfs_navigate_folder(self.eztf_config.get(my_resource, {}))
    for fldr_parent, fldr_path, fldr_name in add_folders:
        create_folder(self, fldr_parent, fldr_path, fldr_name)

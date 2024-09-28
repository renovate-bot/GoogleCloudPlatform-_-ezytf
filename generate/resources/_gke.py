from imports.gke import Gke
from imports.gke_private import GkePrivate
from imports.gke_autopilot import GkeAutopilot
from imports.gke_autopilot_private import GkeAutopilotPrivate


def create_gke(self, gke, gke_type):
    short_gke_id = gke_type.replace("autopilot", "ap").replace("private", "pvt")
    gke_id = f"{short_gke_id}_{gke['name']}"

    gke["project_id"] = self.tf_ref("project", gke["project_id"])
    gke["network"] = self.tf_ref("network_name", gke["network"])
    if gke.get("network_project_id"):
        gke["network_project_id"] = self.tf_ref("project", gke["network_project_id"])

    if gke_type == "gke":
        Gke(self, gke_id, **gke)
    elif gke_type == "gke_private":
        GkePrivate(self, gke_id, **gke)
    elif gke_type == "gke_autopilot":
        GkeAutopilot(self, gke_id, **gke)
    elif gke_type == "gke_autopilot_private":
        GkeAutopilotPrivate(self, gke_id, **gke)


def generate_gke(self, my_resource, resource):
    """creates gke"""
    for gke in self.eztf_config.get(my_resource, []):
        create_gke(self, gke, resource)

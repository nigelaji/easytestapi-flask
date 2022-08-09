from app.restapis.tester import tester_resources
resources = []
resources.extend(tester_resources)


def register_api(api):
    for resource in resources:
        api.add_resource(resource['resource'], resource['urls'])

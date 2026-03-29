def ironclad_validator(input):
    """
    Validator for OSDAG LCC inputs (global RUC mode only).

    Args:
        input (dict): Project input dictionary.
        suggestions (dict): IRC standard suggestions for sync validation.
    """

    report = {"errors": [], "warnings": [], "info": []}

    if "traffic_and_road_data" in input:
        report["warnings"].append(
            "Global mode enabled. traffic_and_road_data will be ignored."
        )

    return report

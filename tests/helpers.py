from __future__ import annotations

import pandas as pd


def build_dataframe() -> pd.DataFrame:
    """Build a small valid dataset for unit tests."""
    return pd.DataFrame(
        {
            "Administrative": [0, 1, 2],
            "Administrative_Duration": [0.0, 4.0, 8.0],
            "Informational": [0, 1, 0],
            "Informational_Duration": [0.0, 3.2, 0.0],
            "ProductRelated": [1, 4, 9],
            "ProductRelated_Duration": [10.0, 20.0, 40.0],
            "BounceRates": [0.1, 0.05, 0.02],
            "ExitRates": [0.2, 0.1, 0.08],
            "PageValues": [0.0, 20.0, 50.0],
            "SpecialDay": [0.0, 0.0, 0.2],
            "Month": ["Feb", "Mar", "May"],
            "OperatingSystems": [1, 2, 2],
            "Browser": [1, 1, 2],
            "Region": [1, 3, 2],
            "TrafficType": [1, 2, 3],
            "VisitorType": ["Returning_Visitor", "New_Visitor", "Returning_Visitor"],
            "Weekend": [False, True, False],
            "Revenue": [0, 1, 1],
        }
    )

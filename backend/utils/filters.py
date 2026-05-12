import pandas as pd


def apply_filters(df, location=None, paid=None):

    if location:
        df = df[
            df['Location'].str.contains(location, case=False, na=False)
        ]

    if paid == "paid":
        df = df[
            ~df['Stipend'].str.contains(
                'unpaid',
                case=False,
                na=False
            )
        ]

    return df
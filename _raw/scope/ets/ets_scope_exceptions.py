"""
Manual ETS scope exceptions that should be applied on top of the main scope files.

Each record updates a scheme's yearly jurisdiction/sector scope before compilation.
Use this for targeted additions/removals that are clearer to maintain outside the
main scheme scope definitions.
"""

ETS_SCOPE_EXCEPTIONS = [
    {
        "gas": "CO2",
        "scheme_id": "eu_ets",
        "year_from": 2013,
        "year_to": 2024,
        "jurisdictions": ["Denmark", "Sweden"],
        "add_sectors": ["4C1"],
        "comment": "Waste incineration plants included in the EU ETS from phase III onward.",
    },
]

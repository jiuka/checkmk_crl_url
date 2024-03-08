from cmk.graphing.v1 import graphs, metrics, perfometers, Title

metric_ttl = metrics.Metric(
    name="ttl",
    title=Title("CRL Lifetime"),
    unit=metrics.Unit(metrics.TimeNotation()),
    color=metrics.Color.LIGHT_BLUE,
)

perfometer_ttl = perfometers.Perfometer(
    name="ttl",
    focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(10)),
    segments=["ttl"],
)

graph_ttl = graphs.Graph(
    name="crl_url",
    title=Title("CRL Lifetime"),
    compound_lines=["ttl"],
    simple_lines=[
        metrics.WarningOf("ttl"),
        metrics.CriticalOf("ttl"),
    ],
)

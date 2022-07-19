import circuit

control_points = [
    (81.8, 196.0),
    (108.0, 210.0),
    (152.0, 216.0),
    (182.0, 185.6),
    (190.0, 159.0),
    (198.0, 122.0),
    (226.0, 93.0),
    (224.0, 41.0),
    (204.0, 15.0),
    (158.0, 24.0),
    (146.0, 52.0),
    (157.0, 93.0),
    (124.0, 129.0),
    (83.0, 104.0),
    (77.0, 62.0),
    (40.0, 57.0),
    (21.0, 83.0),
    (33.0, 145.0),
    (30.0, 198.0),
    (48.0, 210.0),
]

c = circuit.Circuit(control_points=control_points, track_width=10)
c.draw_circuit()

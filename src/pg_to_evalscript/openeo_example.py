import openeo
from openeo.processes import ProcessBuilder, lt, if_


def mask(value: ProcessBuilder):
    red = value.array_element(0)
    nir = value.array_element(1)
    clm = value.array_element(2)

    ndvi = (nir - red) / (nir + red)

    return if_(lt(clm, 40), ndvi)


test_polygon = {
    "type": "Polygon",
    "coordinates": [
        [
            [12.481616, 42.016518],
            [12.437678, 41.995082],
            [12.542031, 41.942992],
            [12.632654, 41.971595],
            [12.620297, 42.002228],
            [12.481616, 42.016518],
        ]
    ],
}

c = openeo.connect("https://openeo.vito.be/openeo/1.0")
c.authenticate_basic("johndoe", "johndoe123")


sen2cor = c.load_collection(
    "SENTINEL2_L2A_SENTINELHUB", bands=["B04", "B08", "CLP"], temporal_extent=["2020-01-01", "2021-01-01"]
)
sen2cor_masked = sen2cor.reduce_dimension(dimension="bands", reducer=mask)
sen2cor_masked = sen2cor_masked.aggregate_spatial(test_polygon, reducer="median")
print(sen2cor_masked.to_json())
# .download("sen2cor.json",format="JSON")

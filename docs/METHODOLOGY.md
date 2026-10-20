# Methodology

CO2.py implements the **Sustainable Web Design Model (SWDM), version 4**, an open
methodology developed by Wholegrain Digital, Mightybytes, Footsprint, EcoPing and the
Green Web Foundation. It is also the default model of the Green Web Foundation's CO2.js.

- SWDM v4: https://sustainablewebdesign.org/estimating-digital-emissions/
- CO2.js models: https://developers.thegreenwebfoundation.org/co2js/models/overview/

## Formula

For each system segment (data centers, networks, user devices):

```
energy (kWh)      = data transferred (GB) x energy intensity (kWh/GB)
emissions (gCO2e) = energy (kWh) x grid carbon intensity (gCO2e/kWh)
```

Energy intensities (SWDM v4, derived from 5.29 ZB of global transfer):

| Segment      | Operational (kWh/GB) | Embodied (kWh/GB) |
|--------------|----------------------|-------------------|
| Data centers | 0.055                | 0.012             |
| Networks     | 0.059                | 0.013             |
| User devices | 0.080                | 0.081             |
| **Total**    | **0.194**            | **0.106**         |

Operational plus embodied is 0.300 kWh/GB. Embodied emissions (manufacturing) can be
turned off with `include_embodied=False`.

Options, as defined by SWDM:

- **Green hosting factor** (0 to 1): data center energy is multiplied by `1 - factor`.
  Use `1` for a host verified green by the
  [Green Web Foundation](https://www.thegreenwebfoundation.org/).
- **Visitor and cache ratios**: total is multiplied by
  `new_visitor_ratio + return_visitor_ratio x (1 - data_cache_ratio)`. The defaults
  (1, 0, 0) mean every byte is transferred and nothing is cached.

## Grid carbon intensity

- Default: **494 gCO2e/kWh**, the global average SWDM v4 takes from the "World" series of
  [Ember](https://ember-energy.org/data/). SWDM says this figure is updated periodically.
- Country values: Ember API `/v1/carbon-intensity/yearly`
  ([docs](https://api.ember-energy.org/v1/docs)). An API key is required
  (https://ember-energy.org/data/api/). Set `EMBER_API_KEY`.
- Every result reports `grid_intensity_source`: `ember` for a real country value,
  `world_average` when the fallback was used, `custom` for a user-supplied provider.
- Ember data is released under CC BY 4.0
  (https://ember-energy.org/creative-commons/). Credit: Ember.

## Units

Data sizes are decimal gigabytes (1 GB = 10^9 bytes), as in SWDM. Emissions are grams of
CO2-equivalent (gCO2e).

## Limitations

- Data transfer is a proxy for energy use, not a measurement. The SWDM authors discuss
  this on the methodology page.
- The model uses global averages for energy intensity. Real values vary by network,
  device and data center.
- Results are estimates with no uncertainty interval. Use them to compare, not to report
  audited figures.
- Country grid intensity applies one value to all three segments. In practice data
  centers, networks and devices are often in different countries.
- Not suitable for cryptocurrency-related traffic (SWDM excludes it).

## Related work

The Green Web Foundation's [CO2.js](https://github.com/thegreenwebfoundation/co2.js)
is the JavaScript reference implementation of SWDM and the best way to cross-check results.

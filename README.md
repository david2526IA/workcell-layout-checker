# Workcell Layout Checker

An explainable 2D geometry check for early robotics-workcell layout prototypes. Define axis-aligned equipment and restricted-zone rectangles in JSON, declare a minimum clearance, and receive a review report.

## Example

```json
{
  "minimum_clearance": 0.5,
  "equipment": [{"id":"robot","x":0,"y":0,"width":1,"height":1}],
  "restricted_zones": [{"id":"walkway","x":2,"y":0,"width":1,"height":1}]
}
```

```bash
pip install .
workcell-check layout.json --output workcell_report.json
```

## Scope

This is a 2D geometric aid for prototypes and discussions. It does not model robot reach, moving bodies, guarding, access, stopping distance, standards, risk assessment or functional safety. Those require appropriate engineering methods and qualified review.

## Development

```bash
pip install ".[dev]"
pytest -q
```

## License

MIT

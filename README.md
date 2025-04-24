This repo explores using tooling to enforce modularization. How do we enforce that only certain symbols from modules are used and that those symbols adhere to certain requirements?

## Banned API
For example, if we want to enforce that nobody directly uses `sqlite3.connect`, we can use Ruff's [banned-api rule](https://docs.astral.sh/ruff/rules/banned-api/):
```toml
# pyproject.toml
[tool.ruff.lint]
extend-select = ["TID251"]

[tool.ruff.lint.flake8-tidy-imports.banned-api]
"sqlite3.connect".msg = "use lib.db module instead."
```

```py
with sqlite3.connect("") as con:
   # ^ `sqlite3.connect` is banned: use lib.db module instead.
    ...
```

## Interface Boundaries
However, if we want to enforce that _only_ specific imports are used, we might use [Tach](https://docs.gauge.sh/getting-started/introduction) to enforce interface boundaries:
```toml
# tach.toml
[[modules]]
path = "lib.db"
depends_on = []

[[interfaces]]
from = ["lib.db"]
expose = ["connection"]

[[modules]]
path = "providers"
depends_on = ["lib.db"]
```
importing `DB_FILE` from `lib.db` (an implementation detail), results in
```
$ uv run tach check

Interfaces
❌ providers/get_providers.py:3: The path 'lib.db.DB_FILE' is not part of the public interface for 'lib.db'.

If you intended to change an interface, edit the '[[interfaces]]' section of tach.toml.
Otherwise, remove any disallowed imports and consider refactoring.
```

## Module Dependencies
Tach can also be used to define module dependencies:

State that `providers` can depend on `lib.db`, but `server` cannot:
```toml
[[modules]]
path = "lib.db"
depends_on = []

[[interfaces]]
from = ["lib.db"]
expose = ["connection"]

[[modules]]
path = "providers"
depends_on = ["lib.db"]

[[modules]]
path = "server"
depends_on = ["providers"]
```

then, importing `lib.db.connection` in `server/main.py` gives:
```
Internal Dependencies
❌ server/main.py:5: Cannot use 'lib.db.connection'. Module 'server' cannot depend on 'lib.db'.

If you intended to add a new dependency, run 'tach sync' to update your module configuration.
Otherwise, remove any disallowed imports and consider refactoring.
```

A module can be marked as a `utility`, which means that any module can import it. This is distinct from _not_ tracking a module at all, because that doesn't allow controlling the module's dependencies.
```toml
[[modules]]
path = "lib.logging"
depends_on = []
utility = true
```

Glob patterns can also be used, which reduces how many explicit module dependencies need to be defined. The following means that any module in `lib` can depend on any other module in `lib`:
```toml
[[modules]]
path = "lib.*"
depends_on = ["lib.*"]
```

Or you have an `apps` folder which contains every domain which provides service method, then you say each domain can depend only on any other domain's service methods:
```toml
[[modules]]
path = "apps.*"
depends_on = ["apps.*"]

[[interface]]
from = ["apps.providers"]
expose = ["get_providers"]

[[interface]]
from = ["apps.licenses"]
expose = ["get_licenses"]
```

Any more explicitly defined module will override the glob definition for that module.

## Drawbacks
The tool in the Ruby ecosystem has/had some drawbacks and blind spots detailed here: https://shopify.engineering/a-packwerk-retrospective.

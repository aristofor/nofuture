# Changelog

## [1.2.1] - 2026-05-30

### Fixed

- installation sur Linux: un wheel manylinux est publié pour CPython (corrige le fallback en compilation depuis la sdist)

### Added

- support de Python 3.14

### Changed

- passage à l'ABI stable de CPython (abi3-py312): un seul wheel par plateforme couvre Python 3.12+

## [1.2.0] - 2026-02-05

### Breaking

- import principal: `import nofuture` (accès via `nofuture.MayBe` / `nofuture.Result`)

### Added

- exemple de pipeline avec Quart et Websocket

### Changed

- mise à jour PyO3 0.27.2 → 0.28.0
- mise à jour maturin 1.10.2 → 1.11.5 (build-system)

## [1.1.0] - 2026-01-25

### Added

- `__len__()` pour `MayBe` et `Result`: retourne 1 si valeur présente (Just/Ok), 0 sinon (Nothing/Err)
- `__iter__()` pour `MayBe` et `Result`: permet l'itération, unpacking, et utilisation avec builtins/itertools
  - `Just(x)` et `Ok(x)` produisent un élément `[x]`
  - `Nothing` et `Err(...)` produisent zéro élément `[]`
  - Compatible avec: unpacking (`val, = maybe`), for loops, `any()`, `all()`, `sum()`, `min()`, `max()`, `zip()`, `enumerate()`, `itertools.chain()`, etc.
- Exemple `examples/iteration_features.py` démontrant les nouvelles capacités d'itération

### Fixed

- Garantie de cohérence: `bool(x) == (len(x) > 0)` pour tous les cas

## [1.0.3] - 2026-01-05

### Added

- `expect(message)` pour `MayBe` et `Result`: comme `unwrap()` mais avec message d'erreur personnalisé
- `to_option()` pour `MayBe` et `Result`: retourne la valeur ou `None`
- `match(just=..., nothing=...)` pour `MayBe`: pattern matching ergonomique
- `match(ok=..., err=...)` pour `Result`: pattern matching ergonomique (err reçoit msg, code, details)
- `Result.from_dict()`: construit un `Result` depuis un dict (réciproque de `to_dict()`)

### Changed

- L'opérateur `>>` lève désormais un `TypeError` si la fonction ne retourne pas un `MayBe`/`Result`

## [1.0.2] - 2025-12-31

### Added

- Support du typage générique pour `MayBe` et `Result` via `__class_getitem__`
  - Permet d'écrire `MayBe[User]` ou `Result[dict[str, Any], ErrorCodes]`
  - Compatible avec les outils de typage statique (mypy, pyright)

### Changed

- Exemple renommé: `examples/abc.py` → `examples/objects.py`

## [1.0.1] - 2025-12-22

### Changed

- README.md: affichage conforme sur pypi.org

## [1.0.0] - 2025-12-22

### Added

- `MayBe` monad: `just()`, `nothing()`, `map()`, `flat_map()`, opérateurs `>>` et `|`
- `Result` monad: `ok()`, `err()`, `map()`, `map_err()`, `flat_map()`, `and_then()`, `to_dict()`
- Erreurs structurées avec `code` et `details` optionnels
- Type stubs pour autocomplétion (`.pyi`)

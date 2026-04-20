Releasing
=========

This project uses a **pull request** to prepare each release, then a **manual Git tag**
as the only step that starts publication (GitHub Actions builds installers and
creates a GitHub Release when a ``v*`` tag is pushed).

Version sources
---------------

Keep these in sync whenever you cut a release:

- ``__version__`` in ``src/dbs_annotator/__init__.py`` (also used by Hatch / ``dbs-annotator`` metadata)
- ``version`` under ``[tool.briefcase]`` in ``pyproject.toml`` (Briefcase requires a static string)

The automation below updates both, then runs `Towncrier`_ to fold ``newsfragments/``
into ``CHANGELOG.rst``.

.. _Towncrier: https://towncrier.readthedocs.io/

Day-to-day: changelog fragments
-------------------------------

For each user-visible change, add a fragment under ``newsfragments/`` (usually in the
same PR as the change):

.. code-block:: bash

   uv run towncrier create 123.feature.rst

Use a real issue number instead of ``123`` when applicable, or a ``+`` prefix for
small internal-only notes (see Towncrier’s naming rules). Common types include
``feature``, ``bugfix``, ``doc``, ``misc``, and ``removal``.

Option A — Prepare the release PR locally
-----------------------------------------

1. Ensure ``main`` is up to date and you have a **clean** working tree (or pass
   ``--allow-dirty`` only if you intend to include other edits — not recommended).

2. Create a branch (do **not** commit the release bump directly on ``main``):

   .. code-block:: bash

      git checkout main
      git pull
      git checkout -b chore/release-prep-X.Y.Z

3. Run the helper (omit ``--commit`` first if you want to inspect diffs only):

   .. code-block:: bash

      uv sync --dev
      uv run python scripts/release_prepare.py X.Y.Z --dry-run
      uv run python scripts/release_prepare.py X.Y.Z --commit

   Use ``--date YYYY-MM-DD`` if the Towncrier release date should not be “today”.
   Use ``--skip-towncrier`` only in exceptional cases (changelog skipped).

4. Push the branch and open a pull request into ``main``. Wait for CI to pass, then
   merge.

Option B — Prepare the release PR from GitHub Actions
-------------------------------------------------------

1. In GitHub: **Actions** → **CD - Prepare release PR** → **Run workflow**.

2. Enter **Version** (``X.Y.Z`` without a ``v`` prefix). Optionally set **Release date**
   (``YYYY-MM-DD``); otherwise UTC “today” is used.

3. The workflow creates branch ``chore/release-prep-X.Y.Z``, runs the same steps as
   ``scripts/release_prepare.py``, pushes it, and opens a pull request.

4. Review and merge the PR when CI is green.

Publish: tag after merge (deliberate final step)
------------------------------------------------

After the release-prep PR is **merged** into ``main``:

1. Update your local ``main`` and identify the **merge commit** (or use GitHub’s
   suggested SHA for the PR merge).

2. Create an **annotated** tag matching the version (``v`` prefix for the git tag
   only):

   .. code-block:: bash

      git checkout main
      git pull
      git tag -a vX.Y.Z -m "Release vX.Y.Z" <merge_commit_sha>
      git push origin vX.Y.Z

3. That push triggers ``.github/workflows/release.yml`` (tag pattern ``v*``), which
   builds Python wheels and Briefcase artifacts and, when appropriate, publishes a
   GitHub Release.

Do **not** push a ``v*`` tag until the release-prep PR is merged and you are satisfied
with ``CHANGELOG.rst`` and the version numbers on ``main``.

Manual workflow dispatch on ``release.yml`` can still build artifacts without a new
tag; see that workflow’s inputs if you need a one-off build.

Troubleshooting
---------------

- **“Working tree is not clean”** — stash or commit unrelated work, or use a fresh clone.
- **Towncrier fails** — ensure there is at least one valid fragment for the release, or
  confirm ``CHANGELOG.rst`` still contains the line
  ``.. towncrier release notes start`` above which Towncrier inserts new entries.
- **Branch already exists** — delete the remote branch ``chore/release-prep-X.Y.Z`` or
  pick a new branch name before re-running the workflow.

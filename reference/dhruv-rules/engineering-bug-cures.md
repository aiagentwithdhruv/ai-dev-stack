# Engineering Bug Cures — Silent Failures and How to Avoid Them

Battle-tested gotchas from a high-volume product build. Each one caused real lost
time before it became a rule. Stack-specific but vendor/employer-neutral.

---

## Python

### Use `removeprefix`, not `lstrip`, to remove a prefix string
`"path".lstrip("/uploads/")` strips **individual characters** in the set, so it can
eat into the real path. Use `"path".removeprefix("/uploads/")` for true substring
removal.

---

## SQLAlchemy / Postgres

### Cast with `CAST(... AS type)`, not `::type`, inside `text()`
`:id::uuid` inside a SQLAlchemy `text()` block is parsed as two bind parameters
(`:id` then `:`). Use `CAST(:id AS uuid)` instead.

### Inspect the real table before writing service code
Check the actual DB column names (`\d table_name`) before writing service/ORM logic.
Attribute-vs-column mismatches are a top source of silent breakage — the field name
you assume is rarely the field name that shipped.

### Seed functions must be idempotent
If running a seed twice creates duplicates, it is broken. Enforce uniqueness at the
DB level (unique constraints), and prefer scripts over UI "seed" buttons for
anything that writes rows.

---

## FastAPI / Pydantic

### A response schema must list **every** field you intend to render
Pydantic **silently strips** fields that are not declared on the response model. Add
a column to the DB + ORM + service but forget the response schema, and the client
receives nothing — no error, no warning. When adding a field, touch all four layers
in the **same commit**: migration → ORM → service → response schema.

### Specific routes before parameterized routes
Register `/resource/add-item` before `/resource/{id}`, or the literal path gets
captured by the `{id}` pattern.

### Keep names consistent across the layers
Response model field names must match the service attribute names must match the ORM
column names. A 2-minute curl of the endpoint catches mismatches that otherwise cost
multiple round-trips.

---

## React / Next.js

### Never call the same hook twice in one component
Need more values from a hook like `useAuth()`? Add them to the existing destructure.
A second call to the same hook can crash to a blank page.

### A `useEffect` may only reference variables declared above it
If an effect uses a value, the hook/line that creates that value must appear on an
earlier line. Order matters.

### Render table-cell dropdowns through a portal
Table cells use `overflow: hidden`, so a kebab/action menu rendered inside a row gets
clipped at the cell boundary. Render it with
`createPortal(<menu/>, document.body)` and position it absolutely from
`e.currentTarget.getBoundingClientRect()`. Pattern: store `{ top, left, id }` in
state and add a click-outside backdrop.

### Modal scroll-lock needs padding compensation
Setting `document.body.style.overflow = 'hidden'` removes the scrollbar, which shifts
page content sideways by the scrollbar width (~15px). Compensate with
`document.body.style.paddingRight = scrollbarWidth + 'px'` and **restore both** on
close/unmount.

### Guard `<input type="number">` with `min`/`max`
A user can type a value too large for the column and crash the backend with a numeric
overflow. Validate in the UI, not just the DB. For a `NUMERIC(p, s)` column the input
`max` is `10^(p-s) - 1` — e.g. `NUMERIC(6,2)` allows up to `9999.99`, so
`max="9999.99"`.

### Use custom modals, not browser `alert()` / `confirm()`
Native dialogs are blocking, un-themeable, and hard to test. Use app primitives (a
notification banner, a state-based confirm modal). Note the call pattern differs:
`confirm()` is **synchronous**; a state-based modal is **async** — you cannot
drop-in swap one for the other.

### Nav gating must mirror backend RBAC
When you add an admin-only route, also add its nav item to the sidebar's admin-only
filter. A visible link that leads to a 403 is broken UX even though the data is
technically protected.

---

## Multi-tenant

### Every user-lookup query must also filter by tenant
A `WHERE email = ?` query without a tenant filter can match the same person across
multiple tenants and raise a multiple-results error. Always add the tenant predicate
to identity lookups.

---

## Local build & environment hygiene

### Build before you open the browser
After a code change, run the build first. If the build fails, fix it before testing
in the browser — runtime errors do not always show up in a passing build, but build
errors guarantee the page is stale.

### Clear the dev bundler cache after any git operation
After a `git reset`, `revert`, or branch switch, remove the bundler cache
(e.g. `rm -rf node_modules/.vite`) and restart the dev server. A stale cache serves
old, broken code even when the files on disk are correct.

### Stop stray containers before local dev
A leftover Docker container holding a port silently serves old code. Stop containers
before starting a local server on the same port.

### Read the exact error before changing code
Read the actual error message / traceback before pattern-matching a fix. Grep the
log for the error first — the console usually tells you exactly what is wrong.

### Keep auth provider keys aligned across all surfaces
Frontend build args, backend env, and any worker env must point at the **same** auth
provider project. A mismatch fails auth everywhere at once.

### Every backend service needs its proxy route
A backend service with no matching reverse-proxy (e.g. nginx) route returns 404/405
on deploy. Add the route before building images.

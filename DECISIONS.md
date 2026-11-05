# Decisions

The choices that shaped CougarConnect, what was weighed against them, and what each one costs. Commit references point to where the decision landed.

## 1. One Postgres database, reached two ways

**Chosen:** a single Supabase Postgres instance holds everything. ASP.NET Core Identity reaches its account tables through EF Core (Npgsql). The alumni domain data (`Alumni`, `Messages`, `ConnectionRequests`, `Notifications`) is reached over Supabase's PostgREST API through `HttpClient` in `SupabaseService`.

**Why:** the domain data already lived in Supabase and was read over REST from the 2024 version. Identity originally ran on SQL Server. Moving Identity into the same Postgres instance (`e3ab6b2`) meant the live demo needed one database instead of two, and no SQL Server host.

**Rejected:** keeping SQL Server for Identity (a second, heavier database to host for a free-tier demo); moving the domain data to EF Core as well (a rewrite of every page's data access for no user-visible change).

**Cost:** two data-access styles in one app. There are no transactions spanning the two paths, and the schema is split: EF Core migrations own the Identity tables and `supabase/schema.sql` owns the domain tables.

## 2. SQL Server, then SQLite, then Postgres

**Chosen:** PostgreSQL, via Supabase.

**History:** the 2024 project ran Identity on SQL Server LocalDB, which in practice meant
Windows and Visual Studio just to run the app locally. A June 2026 attempt swapped Identity
to SQLite (`cougarconnect/sqlite-cleanup`, never merged) to remove the database-server
requirement entirely. It was dropped in July for Postgres (`e3ab6b2`): the alumni data
already lived in Supabase Postgres, so moving Identity there gave the live demo a single
database. A SQLite file would have been a second data store, and Render's free tier has no
persistent disk, so the file would have been wiped on every redeploy.

**Cost:** none still carried in the code; the SQLite branch is abandoned.
## 3. Row Level Security off; the anon key stays on the server

**Chosen:** RLS is disabled on the four domain tables, and every PostgREST call uses the anon key from the server.

**Why:** this is a Blazor Server app, so all data access runs on the server and the key is never sent to the browser. Per-user authorization is already enforced by Identity before any query runs. RLS policies would need a per-user Postgres identity, meaning Supabase Auth or minting Supabase-compatible JWTs, which duplicates the Identity layer.

**Cost:** the anon key is effectively full read/write on those tables. Its secrecy is the whole control: it lives only in the host's environment variables and is never committed. If the app ever moved to client-side rendering, RLS would have to come back.

## 4. Identity migrations apply at startup

**Chosen:** `db.Database.Migrate()` runs when the app boots, guarded by `IsRelational()` so it's a no-op under the in-memory provider the integration tests use.

**Why:** a freshly provisioned database, such as a new Supabase project behind a new deploy, gets the Identity schema with no manual step.

**Cost:** any deploy that includes a new migration applies DDL to the live database automatically, with no review step. Acceptable for a demo with one schema owner; it would not be for a shared production database.

## 5. Email confirmation is not required to sign in

**Chosen:** `RequireConfirmedAccount = false`, and every email send is wrapped so an SMTP failure can't crash the request (`1dfe897`).

**Why:** the only SMTP sender available is a shared credential that can't be rotated, so confirmation and reset mail isn't reliably delivered. With confirmation required, every self-registered user was locked out of the live demo, and a failed send turned "Forgot password" into a 500 page.

**Cost:** an account can be registered with an address the user doesn't own. Password reset by email is best-effort.

## 6. One search box across every field

**Chosen:** a single search term matched case-insensitively against name, graduation year, city, major and company, as one PostgREST `or=(…ilike.*term*…)` query.

**Rejected:** per-field filters (users would have to know which field to pick) and Postgres full-text search with `tsvector` (more setup than a directory this size needs).

**Cost:** a leading-wildcard `ILIKE` can't use a btree index, so every search scans the `Alumni` table. Fine at demo size; a larger directory would need a trigram (`pg_trgm`) index or full-text search.

## 7. Render's free tier for the app, Supabase for the database

**Chosen:** the app runs as a Docker container on Render's free tier (`render.yaml`), backed by Supabase Postgres.

**Rejected:** Render's free Postgres, which is deleted after 30 days.

**Cost:** the service sleeps when idle, so the first request takes about 50 seconds to wake it. Free-tier limits also forced `DOTNET_hostBuilder__reloadConfigOnChange=false` in the Dockerfile: the default config file watchers exhausted the host's inotify limit and crashed the app at startup.

## 8. Blazor Server

**Chosen:** Blazor Server, inherited from the 2024 project's template.

**Consequences, good and bad:** it's what makes decision 3 safe, because the browser never sees a database key. Every interaction is a SignalR round trip, so the UI is only as responsive as the connection. When the free-tier host sleeps or restarts, open sessions drop their circuit and have to reload.

## Smaller records

* **Exact-match lookup by id** (`c04f6de`). Looking up an alumnus by numeric id went through the same `ilike` helper as search, and PostgREST rejects `ilike` on a `bigint` column. It broke the Connections and Recent Activity pages for every account with a connection. Fixed with a dedicated `GetAlumniById` that uses `id=eq.{id}`.
* **No leaking request headers.** A header set for one PostgREST call carried over into the next call on the shared `HttpClient`. There's now a regression test: `PostData_SecondCall_DoesNotLeakPreferHeadersFromFirstCall`.

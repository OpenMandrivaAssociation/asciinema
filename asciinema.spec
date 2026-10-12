Name:		asciinema
Version:	3.2.1
Release:	2
Summary:	Terminal session recorder
License:	GPLv3
Group:		Development/Other
URL:		https://docs.asciinema.org/
Source0:	https://github.com/asciinema/asciinema/archive/refs/tags/v%{version}.tar.gz
Source1:	%{name}-%{version}-vendor.tar.xz
BuildRequires:	cargo
BuildRequires:	rust

%description
asciinema records terminal sessions and plays them back. Version 3 is a
Rust program. The crates are vendored because package builds have no network.

%prep
%autosetup -n %{name}-%{version} -a1
mkdir -p .cargo
cat >> .cargo/config.toml << 'EOF'

[net]
offline = true

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
export CARGO_NET_OFFLINE=true
export CARGO_HOME=$PWD/.cargo
# rpm's find-debuginfo strips the binary. The upstream profile strips it first.
export CARGO_PROFILE_RELEASE_STRIP=false
export CARGO_PROFILE_RELEASE_DEBUG=line-tables-only
cargo build --release --offline --locked
cargo tree --offline --locked --edges no-build,no-dev,no-proc-macro --prefix none --format '{l}: {p}' \
	| sed -e "s: ($PWD[^)]*)::g" -e 's: / :/:g' -e 's:/: OR :g' \
	| sort -u > LICENSES.dependencies
test -n "$(find target/release/build -type f -path '*/out/man/*.1' -print -quit)"

%install
install -Dm755 target/release/asciinema %{buildroot}%{_bindir}/asciinema
mkdir -p %{buildroot}%{_mandir}/man1
find target/release/build -type f -path '*/out/man/*.1' -print0 |
	xargs -0 -I{} install -m644 {} %{buildroot}%{_mandir}/man1/

%files
%license LICENSE LICENSES.dependencies
%doc README.md
%{_bindir}/asciinema
%{_mandir}/man1/asciinema*.1*

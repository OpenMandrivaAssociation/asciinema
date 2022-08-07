%global upstream asciinema
%global gitbase  https://github.com

Summary: Terminal session recorder
Name:    asciinema
Version: 2.2.0
Release: %mkrel 1
License: GPLv3
Url:     https://%{upstream}.github.io/%{name}
Source0: %{gitbase}/%{upstream}/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildArch: noarch

BuildRequires: pkgconfig(python3)
BuildRequires: python-wheel
BuildRequires: python-pip

%description
asciinema lets you easily record terminal sessions
and replay them in a terminal as well as in a web browser.

%prep
%autosetup -n %{name}-%{version}

%build
mkdir wheels
pip wheel --wheel-dir wheels --no-deps --no-build-isolation --verbose .

%install
pip install --root=%{buildroot} --no-deps --verbose --ignore-installed --no-warn-script-location --no-index --no-cache-dir --find-links wheels wheels/*.whl

rm %{buildroot}%{_docdir}/%{name}/{CODE_OF_CONDUCT,CONTRIBUTING}.md

%files
%license LICENSE
%doc %{_docdir}/%{name}
%{_bindir}/%{name}
%{_mandir}/man*/%{name}.*
%{py_sitedir}/%{name}
%{py_sitedir}/%{name}-%{version}.dist-info

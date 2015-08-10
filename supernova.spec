Name:           supernova
Version:        2.0.8
Release:        2%{?dist}
Summary:        Use novaclient with multiple OpenStack nova environments the easy way
License:        ASL 2.0
URL:            https://github.com/major/supernova
Source0:        https://pypi.python.org/packages/source/s/supernova/supernova-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  pytest
BuildRequires:  python-click
BuildRequires:  python-configobj
BuildRequires:  python-coverage
BuildRequires:  python-devel
BuildRequires:  python-keyring
BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python-tox
Requires:       python-click
Requires:       python-configobj
Requires:       python-keyring
Requires:       python-novaclient
Requires:       pycryptopp
Requires:       python-simplejson
Requires:       python-six
Requires:       python-iso8601


%description
supernova manages multiple nova environments without sourcing
novarc's or mucking with environment variables.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
PYTHONPATH=$(pwd) py.test tests --tb=long --verbose

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/supernova
%{_bindir}/supernova-keyring

%dir %{python_sitelib}/%{name}
%{python_sitelib}/%{name}/*.py
%{python_sitelib}/%{name}/*.pyc
%{python_sitelib}/%{name}/*.pyo

%dir %{python_sitelib}/supernova-*-py?.?.egg-info
%{python_sitelib}/supernova-*-py?.?.egg-info/*

%changelog
* Sun Aug 09 2015 Major Hayden <major@mhtx.net> - 2.0.8-2
- Adding python-six to BuildRequires 

* Sun Aug 09 2015 Major Hayden <major@mhtx.net> - 2.0.8-1
- Version bump and spec improvements

* Thu Aug 06 2015 Major Hayden <major@mhtx.net> - 2.0.7-1
- Version bump

* Wed Aug 05 2015 Major Hayden <major@mhtx.net> - 2.0.6-1
- Version bump

* Fri Jul 31 2015 Major Hayden <major@mhtx.net> - 2.0.5-1
- Version bump

* Fri Jul 31 2015 Major Hayden <major@mhtx.net> - 2.0.4-2
- Use more basic python packaging format

* Wed Jul 29 2015 Major Hayden <major@mhtx.net> - 2.0.4-1
- Version bump

* Fri Jul 24 2015 Major Hayden <major@mhtx.net> - 2.0.3-1
- Version bump

* Tue Jul 21 2015 Major Hayden <major@mhtx.net> - 2.0.2-1
- Version bump

* Tue Jul 21 2015 Major Hayden <major@mhtx.net> - 2.0.0-3
- Python3 packaging

* Tue Jul 21 2015 Major Hayden <major@mhtx.net> - 2.0.0-2
- Bug fixes in spec file

* Tue Jul 21 2015 Major Hayden <major@mhtx.net> - 2.0.0-1
- Version bump to 2.0.0

* Tue Oct 28 2014 Jason DeTiberus <jdetiber@redhat.com> - 1.0.7-1
- version bump to 1.0.7

* Fri Jun 20 2014 Carl George <carl@carlgeorge.us> - 1.0.1-1
- Version bump to 1.0.1
- Follow Fedora Python packaging guidelines

* Thu May 29 2014 Greg Swift <gregswift@gmail.com> - 1.0.0-1
- Version bump to 1.0.0

* Thu May 01 2014 Major Hayden <major@mhtx.net> - 0.9.6-1
- Version bump to 0.9.6

* Mon Jan 13 2014 Major Hayden <major@mhtx.net> - 0.9.0-1
- Version bump to 0.9.0

* Mon Jan 28 2013 Greg Swift <gregswift@gmail.com> - 0.7.5-2
- Added iso8601 dependency

* Mon Jan 28 2013 Greg Swift <gregswift@gmail.com> - 0.7.5-1
- Initial creation of spec file

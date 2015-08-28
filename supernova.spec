# python-novaclient doesn't have a python 3 package at this time
%global with_python3 0

Name:           supernova
Version:        2.0.9
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
novarc files or mucking with environment variables.

%if 0%{?with_python3}
%package -n python3-supernova
Summary:        Use novaclient with multiple OpenStack nova environments the easy way
BuildRequires:  pytest
BuildRequires:  python3-click
BuildRequires:  python3-configobj
BuildRequires:  python3-coverage
BuildRequires:  python3-devel
BuildRequires:  python3-keyring
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python-tox
Requires:       python3-click
Requires:       python3-configobj
Requires:       python3-keyring
Requires:       python3-novaclient
Requires:       pycryptopp
Requires:       python3-simplejson
Requires:       python3-six
Requires:       python3-iso8601

%description -n python3-supernova
supernova manages multiple nova environments without sourcing
novarc files or mucking with environment variables.

%endif # with_python3

%package -n supernova-doc
Summary:    Documentation for supernova

%description -n supernova-doc
supernova-doc contains documentation and sample conifiguration files for use
with supernova.

%prep
%setup -q

%build
%if 0%{?with_python3}
%{__python3} setup.py build
mv build build3
%endif

%{__python2} setup.py build
mv build build2

%install
mv build2 build
%{__python2} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}/%{_bindir}/supernova %{buildroot}/%{_bindir}/supernova2
mv %{buildroot}/%{_bindir}/supernova-keyring %{buildroot}/%{_bindir}/supernova-keyring2
rm -rf build

%if 0%{?with_python3}
mv build3 build
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}/%{_bindir}/supernova %{buildroot}/%{_bindir}/supernova%{python3_version}
mv %{buildroot}/%{_bindir}/supernova-keyring %{buildroot}/%{_bindir}/supernova-keyring%{python3_version}
%endif

ln -s %{_bindir}/supernova2 %{buildroot}/%{_bindir}/supernova
ln -s %{_bindir}/supernova-keyring2 %{buildroot}/%{_bindir}/supernova-keyring

%check
PYTHONPATH=$(pwd) py.test tests --tb=long --verbose

%files
%{_bindir}/supernova
%{_bindir}/supernova2
%{_bindir}/supernova-keyring
%{_bindir}/supernova-keyring2
%{python2_sitelib}/supernova-%{version}-py%{python2_version}.egg-info
%{python2_sitelib}/supernova
%license LICENSE

%if 0%{?with_python3}
%files -n python3-supernova
%{_bindir}/supernova%{python3_version}
%{_bindir}/supernova-keyring%{python3_version}
%{python3_sitelib}/supernova-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/supernova
%license LICENSE
%endif

%files -n supernova-doc
%doc docs/ example_configs
%license LICENSE

%changelog
* Fri Aug 28 2015 Major Hayden <major@mhtx.net> - 2.0.9-2
- Disable python 3 build since python3-novaclient doesn't exist yet

* Thu Aug 27 2015 Major Hayden <major@mhtx.net> - 2.0.9-1
- New upstream version

* Thu Aug 27 2015 Major Hayden <major@mhtx.net> - 2.0.8-4
- Added python3 and doc subpackages

* Wed Aug 26 2015 Major Hayden <major@mhtx.net> - 2.0.8-3
- Cleanup

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

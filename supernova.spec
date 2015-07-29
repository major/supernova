%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

%if 0%{?fedora} && 0%{?fedora} >= 18
%global with_python3 1
%endif

Name:           python-supernova
Version:        2.0.4
Release:        1%{?dist}
Summary:        Use novaclient with multiple OpenStack nova environments the easy way
License:        ASLv2
URL:            https://github.com/major/supernova
Source0:        https://pypi.python.org/packages/source/s/supernova/supernova-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

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

%if 0%{?with_python3}
%package -n python3-supernova
Summary:        Use novaclient with multiple OpenStack nova environments the easy way

%description -n python3-supernova
supernova manages multiple nova environments without sourcing
novarc's or mucking with environment variables.
%endif

%prep
%setup -qc
mv supernova-%{version} python2

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find python2 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%build
pushd python2
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build
popd

%if 0%{?with_python3}
pushd python3
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

pushd python2
%{__python2} setup.py install --skip-build --root %{buildroot}
popd

%files
%{python2_sitelib}/*
%{_bindir}/supernova
%{_bindir}/supernova-keyring

%if 0%{?with_python3}
%files -n python3-supernova
%{python3_sitelib}/*
%{_bindir}/supernova
%{_bindir}/supernova-keyring
%endif

%changelog
* Wed Jul 29 2015 Major Hayden <major@mhtx.net> - 2.0.4-1
* Version bump

* Fri Jul 24 2015 Major Hayden <major@mhtx.net> - 2.0.3-1
* Version bump

* Tue Jul 21 2015 Major Hayden <major@mhtx.net> - 2.0.2-1
* Version bump

* Tue Jul 21 2015 Major Hayden <major@mhtx.net> - 2.0.0-3
* Python3 packaging

* Tue Jul 21 2015 Major Hayden <major@mhtx.net> - 2.0.0-2
* Bug fixes in spec file

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

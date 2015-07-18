%if 0%{?fedora} < 13
%global __python2 %{_bindir}/python2
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

Name:           supernova
Version:        2.0.0
Release:        1%{?dist}
Summary:        Use novaclient with multiple OpenStack nova environments the easy way
License:        ASLv2
URL:            https://github.com/major/supernova
Source0:        https://pypi.python.org/packages/source/s/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-setuptools
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
%{__python2} setup.py build


%install
%{__python2} setup.py install --optimize 1 --skip-build --root %{buildroot}


%files
%{python2_sitelib}/*
%{_bindir}/supernova
%{_bindir}/supernova-keyring


%changelog
* Tue Oct 28 2014 Jason DeTiberus <jdetiber@redhat.com> - 1.0.7-1
- version bump to 1.0.7

* Fri Jun 20 2014 Carl George <carl@carlgeorge.us> - 1.0.1-1
- Version bump to 1.0.1
- Follow Fedora Python packaging guidelines

* Thu May 29 2014 Greg Swift <gregswift@gmail.com> - 1.0.0-1
- Version bump to 1.0.0

* Mon May 1 2014 Major Hayden <major@mhtx.net> - 0.9.6-1
- Version bump to 0.9.6

* Mon Jan 13 2014 Major Hayden <major@mhtx.net> - 0.9.0-1
- Version bump to 0.9.0

* Mon Jan 28 2013 Greg Swift <gregswift@gmail.com> - 0.7.5-2
- Added iso8601 dependency

* Mon Jan 28 2013 Greg Swift <gregswift@gmail.com> - 0.7.5-1
- Initial creation of spec file

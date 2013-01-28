%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           supernova
Version:        0.7.5
Release:        2%{?dist}
Summary:        Use novaclient with multiple OpenStack nova environments the easy way

License:        ASLv2
URL:            https://github.com/rackerhacker/supernova
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-setuptools
Requires:       python-keyring
Requires:       python-novaclient
Requires:       pycryptopp
Requires:       python-simplejson
Requires:       python-iso8601

%description
supernova manages multiple nova environments without sourcing
novarc's or mucking with environment variables.

%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%{python_sitelib}/*
%{_bindir}/supernova
%{_bindir}/supernova-keyring

%changelog
* Mon Jan 28 2013 Greg Swift <gregswift@gmail.com> - 0.7.5-2
-Added iso8601 dependency

* Mon Jan 28 2013 Greg Swift <gregswift@gmail.com> - 0.7.5-1
- Initial creation of spec file

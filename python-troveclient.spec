%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname troveclient
%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
This is a client for the Trove API. There's a Python API (the \
troveclient module), and a command-line script (trove). Each \
implements 100% (or less ;) ) of the Trove API.

Name:           python-troveclient
Version:        XXX
Release:        XXX
Summary:        Client library for OpenStack DBaaS API

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  git


%description
%{common_desc}

%package -n python2-%{sname}
Summary:        Client library for OpenStack DBaaS API
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx
BuildRequires:  python2-requests
BuildRequires:  python2-pbr
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-oslotest
BuildRequires:  python2-mock
BuildRequires:  python2-testtools
BuildRequires:  python2-keystoneauth1
BuildRequires:  python2-keystoneclient
BuildRequires:  python2-mistralclient
BuildRequires:  python2-swiftclient
BuildRequires:  python2-httplib2
BuildRequires:  python2-crypto
%if 0%{?fedora} > 0
BuildRequires:  python2-testrepository
BuildRequires:  python2-simplejson
BuildRequires:  python2-requests-mock
%else
BuildRequires:  python-testrepository
BuildRequires:  python-simplejson
BuildRequires:  python-requests-mock
%endif

Requires:       python2-babel
Requires:       python2-keystoneauth1 >= 3.3.0
Requires:       python2-keystoneclient
Requires:       python2-mistralclient >= 3.1.0
Requires:       python2-swiftclient >= 3.2.0
Requires:       python2-osc-lib >= 1.8.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-pbr
Requires:       python2-prettytable
Requires:       python2-requests
Requires:       python2-six
%if 0%{?fedora} > 0
Requires:       python2-simplejson
%else
Requires:       python2-simplejson
%endif

%{?python_provide:%python_provide python2-%{sname}}

%description -n python2-%{sname}
%{common_desc}


%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:        Client library for OpenStack DBaaS API
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-requests
BuildRequires:  python3-pbr
BuildRequires:  python3-oslotest
BuildRequires:  python3-mock
BuildRequires:  python3-testtools
BuildRequires:  python3-testrepository
BuildRequires:  python3-keystoneclient
BuildRequires:  python3-mistralclient
BuildRequires:  python3-swiftclient
BuildRequires:  python3-simplejson
BuildRequires:  python3-httplib2
BuildRequires:  python3-requests-mock
BuildRequires:  python3-crypto

Requires:       python3-babel
Requires:       python3-keystoneauth1 >= 3.3.0
Requires:       python3-keystoneclient
Requires:       python3-mistralclient >= 3.1.0
Requires:       python3-swiftclient >= 3.2.0
Requires:       python3-osc-lib >= 1.8.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-pbr
Requires:       python3-prettytable
Requires:       python3-requests
Requires:       python3-simplejson
Requires:       python3-six

%{?python_provide:%python_provide python3-%{sname}}

%description -n python3-%{sname}
%{common_desc}
%endif


%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf %{name}.egg-info

# Let RPM handle the requirements
rm -f {test-,}requirements.txt


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%{__python2} setup.py build_sphinx -b html


%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/trove %{buildroot}%{_bindir}/trove-%{python3_version}
ln -s ./trove-%{python3_version} %{buildroot}%{_bindir}/trove-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/trove %{buildroot}%{_bindir}/trove-%{python2_version}
ln -s ./trove-%{python2_version} %{buildroot}%{_bindir}/trove-2

ln -s ./trove-2 %{buildroot}%{_bindir}/trove


%check
PYTHONPATH=. %{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
PYTHONPATH=. %{__python3} setup.py test
%endif


%files -n python2-%{sname}
%doc doc/build/html README.rst
%license LICENSE
%{python2_sitelib}/python_troveclient-*.egg-info
%{python2_sitelib}/troveclient
%{_bindir}/trove-2*
%{_bindir}/trove

%if 0%{?with_python3}
%files -n python3-%{sname}
%doc doc/build/html README.rst
%license LICENSE
%{python3_sitelib}/python_troveclient-*.egg-info
%{python3_sitelib}/troveclient
%{_bindir}/trove-3*
%endif

%changelog

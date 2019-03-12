# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname troveclient
%global with_doc 1

%global common_desc \
This is a client for the Trove API. There's a Python API (the \
troveclient module), and a command-line script (trove). Each \
implements 100% (or less ;) ) of the Trove API.

Name:           python-troveclient
Version:        2.17.0
Release:        1%{?dist}
Summary:        Client library for OpenStack DBaaS API

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  git


%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:        Client library for OpenStack DBaaS API
%{?python_provide:%python_provide python%{pyver}-%{sname}}
%if %{pyver} == 3
Obsoletes: python2-%{sname} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-requests
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-keystoneclient
BuildRequires:  python%{pyver}-mistralclient
BuildRequires:  python%{pyver}-swiftclient
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-crypto
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-simplejson
BuildRequires:  python-requests-mock
BuildRequires:  python-httplib2
%else
BuildRequires:  python%{pyver}-simplejson
BuildRequires:  python%{pyver}-requests-mock
BuildRequires:  python%{pyver}-httplib2
%endif

Requires:       python%{pyver}-babel
Requires:       python%{pyver}-keystoneauth1 >= 3.4.0
Requires:       python%{pyver}-keystoneclient
Requires:       python%{pyver}-mistralclient >= 3.1.0
Requires:       python%{pyver}-swiftclient >= 3.2.0
Requires:       python%{pyver}-osc-lib >= 1.10.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-prettytable
Requires:       python%{pyver}-requests
Requires:       python%{pyver}-six
# Handle python2 exception
%if %{pyver} == 2
Requires:       python-simplejson
%else
Requires:       python%{pyver}-simplejson
%endif

%description -n python%{pyver}-%{sname}
%{common_desc}


%if 0%{?with_doc}
%package doc
Summary:        Documentation for troveclient
# These are doc requirements
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-sphinxcontrib-apidoc
%description doc
%{common_desc}

This package contains the documentation
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf %{name}.egg-info

# Let RPM handle the requirements
rm -f {test-,}requirements.txt


%build
%{pyver_build}

%install
%{pyver_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s trove %{buildroot}%{_bindir}/trove-%{pyver}


%if 0%{?with_doc}
# generate html docs
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%check
export PYTHON=%{pyver_bin}
PYTHONPATH=. %{pyver_bin} setup.py test


%files -n python%{pyver}-%{sname}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/python_troveclient-*.egg-info
%{pyver_sitelib}/troveclient
%{_bindir}/trove-%{pyver}
%{_bindir}/trove

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Tue Mar 12 2019 RDO <dev@lists.rdoproject.org> 2.17.0-1
- Update to 2.17.0


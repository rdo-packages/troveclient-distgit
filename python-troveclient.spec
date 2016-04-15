%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:           python-troveclient
Version:        2.1.1
Release:        1%{?dist}
Summary:        Client library for OpenStack DBaaS API

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}%{?milestone}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-requests
BuildRequires:  python-pbr
BuildRequires:  python-oslo-sphinx

Requires:       python-argparse
Requires:       python-keystoneclient
Requires:       python-oslo-utils
Requires:       python-pbr
Requires:       python-prettytable
Requires:       python-requests
Requires:       python-setuptools
Requires:       python-simplejson
Requires:       python-six

# required for tests
# tests currently disabled due missing deps
#BuildRequires:  python-pep8
#BuildRequires:  pyflakes
# currently under review
# https://bugzilla.redhat.com/show_bug.cgi?id=839056
# BuildRequires:  python-flake8

# Currently under review
# https://bugzilla.redhat.com/show_bug.cgi?id=958007
# BuildRequires:  python-hacking
#BuildRequires: python-mock
#BuildRequires: python-testtools
#BuildRequires: python-testrepository

%description
This is a client for the Trove API. There's a Python API (the
troveclient module), and a command-line script (trove). Each
implements 100% (or less ;) ) of the Trove API.

%prep
%setup -q -n %{name}-%{upstream_version}

# Remove bundled egg-info
rm -rf %{name}.egg-info

# Let RPM handle the requirements
rm -f {test-,}requirements.txt

# Generate html docs
#export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%build
%if 0%{?rhel} == 6
%{__python} setup.py build
%else
%{__python2} setup.py build
%endif


%install
%if 0%{?rhel} == 6
%{__python} setup.py install --skip-build --root %{buildroot}
%else
%{__python2} setup.py install --skip-build --root %{buildroot}
%endif

# currently disabling tests
# see buildrequires
#%check
#%{__python2} setup.py test


%files
%doc html README.rst LICENSE
%if 0%{?rhel} == 6
%{python_sitelib}/python_troveclient-*.egg-info
%{python_sitelib}/troveclient
%else
%{python2_sitelib}/python_troveclient-*.egg-info
%{python2_sitelib}/troveclient
%endif
%{_bindir}/trove

%changelog
* Wed Mar 23 2016 RDO <rdo-list@redhat.com> 2.1.1-0.1
-  Rebuild for Mitaka 2.1.1

Name:           python-troveclient
Version:        1.0.9
Release:        1%{?dist}
Summary:        Client library for OpenStack DBaaS API

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-requests
BuildRequires:  python-pbr

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
%setup -q -n %{name}-%{version}

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
%{python_sitelib}/python_troveclient-%{version}-py?.?.egg-info
%{python_sitelib}/troveclient
%else
%{python2_sitelib}/python_troveclient-%{version}-py?.?.egg-info
%{python2_sitelib}/troveclient
%endif
%{_bindir}/trove

%changelog
* Tue Mar 31 2015 Haikel Guemar <hguemar@fedoraproject.org> 1.0.9-1
- Update to upstream 1.0.9

* Mon Oct 13 2014 Jakub Ruzicka <jruzicka@redhat.com> 1.0.7-1
- Update to upstream 1.0.7

* Mon Jun 16 2014 Jakub Ruzicka <jruzicka@redhat.com> 1.0.5-1
- Update to upstream 1.0.5
- Add missing dependencies
- Align .spec file with other *client packages
- Remove now unneeded python-spinx10 conditionals

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 08 2014 Matthias Runge <mrunge@redhat.com> - 1.0.3-2
- remove runtime dep to pbr

* Fri Dec 06 2013 Matthias Runge <mrunge@redhat.com> - 1.0.3-1
- upgrade to 1.0.3

* Tue Sep 17 2013 Matthias Runge <mrunge@redhat.com> - 0.1.4-3
- also build on EPEL6

* Thu Sep 12 2013 Matthias Runge <mrunge@redhat.com> - 0.1.4-2
- change {__python} to {__python2}

* Thu Sep 12 2013 Matthias Runge <mrunge@redhat.com> - 0.1.4-1
- Initial package.

#
# Conditional build:
%bcond_with	tests	# unit tests

Summary:	An RST directive for injecting a Towncrier-generated changelog draft containing fragments for the unreleased (next) project version
Name:		python3-sphinxcontrib-towncrier
Version:	0.2.0a0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinxcontrib-towncrier/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinxcontrib-towncrier/sphinxcontrib-towncrier-%{version}.tar.gz
# Source0-md5:	556b38e82f42426d6dcc61ad2303ef4d
URL:		https://pypi.org/project/sphinxcontrib-towncrier/
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Sphinx >= 1.7
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An RST directive for injecting a Towncrier-generated changelog draft
containing fragments for the unreleased (next) project version.

%prep
%setup -q -n sphinxcontrib-towncrier-%{version}

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/sphinxcontrib/towncrier
%{py3_sitescriptdir}/sphinxcontrib_towncrier-%{version}-py*.egg-info

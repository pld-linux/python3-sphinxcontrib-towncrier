#
# Conditional build:
%bcond_with	tests	# unit tests
%bcond_without	doc	# Sphinx documentation

Summary:	An RST directive for injecting a Towncrier-generated changelog draft containing fragments for the unreleased (next) project version
Summary(pl.UTF-8):	Dyrektywa RST do wstawiania szablonu logu zmian z Towncriera, zawierającego fragmenty dla kolejnej wersji projektu
Name:		python3-sphinxcontrib-towncrier
Version:	0.5.0a0
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinxcontrib-towncrier/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinxcontrib-towncrier/sphinxcontrib_towncrier-%{version}.tar.gz
# Source0-md5:	ccbfe2f9442ee2eb10cdc98313226e3f
URL:		https://pypi.org/project/sphinxcontrib-towncrier/
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:64
BuildRequires:	python3-setuptools_scm >= 8
%if %{with tests}
BuildRequires:	python3-Sphinx >= 3.5.1
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-xdist
BuildRequires:	python3-towncrier >= 23
%endif
%if %{with doc}
BuildRequires:	python3-furo >= 2021.02.28.beta28
BuildRequires:	python3-myst_parser >= 0.13.5
BuildRequires:	python3-sphinxcontrib-apidoc >= 0.3.0
BuildRequires:	python3-towncrier >= 23
BuildRequires:	sphinx-pdg >= 3.5.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An RST directive for injecting a Towncrier-generated changelog draft
containing fragments for the unreleased (next) project version.

%description -l pl.UTF-8
Dyrektywa RST do wstawiania szablonu logu zmian z Towncriera,
zawierającego fragmenty dla nie wydanej (kolejnej) wersji projektu.

%package apidocs
Summary:	API documentation for Python sphinxcontrib.towncrier module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sphinxcontrib.towncrier
Group:		Documentation

%description apidocs
API documentation for Python sphinxcontrib.towncrier module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sphinxcontrib.towncrier.

%prep
%setup -q -n sphinxcontrib_towncrier-%{version}

%{__sed} -i -e '/^get_scm_version/ s/=.*/= lambda **kwargs : "%{version}"/' docs/conf.py

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="xdist.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 docs docs/_build/html
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

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,pkg,*.html,*.js}
%endif

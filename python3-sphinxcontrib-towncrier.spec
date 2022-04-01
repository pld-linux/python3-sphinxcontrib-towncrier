#
# Conditional build:
%bcond_with	tests	# unit tests
%bcond_without	doc	# Sphinx documentation

Summary:	An RST directive for injecting a Towncrier-generated changelog draft containing fragments for the unreleased (next) project version
Summary(pl.UTF-8):	Dyrektywa RST do wstawiania szablonu logu zmian z Towncriera, zawierającego fragmenty dla kolejnej wersji projektu
Name:		python3-sphinxcontrib-towncrier
Version:	0.2.1a0
Release:	4
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinxcontrib-towncrier/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinxcontrib-towncrier/sphinxcontrib-towncrier-%{version}.tar.gz
# Source0-md5:	b315d29674b2af992e98ef762bcc9de0
URL:		https://pypi.org/project/sphinxcontrib-towncrier/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 3.5
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-Sphinx >= 1.7
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-xdist
BuildRequires:	python3-towncrier >= 19.2
%endif
%if %{with doc}
BuildRequires:	python3-furo >= 2021.02.28.beta28
BuildRequires:	python3-myst_parser >= 0.13.5
BuildRequires:	python3-sphinxcontrib-apidoc >= 0.3.0
# already installed package
BuildRequires:	python3-sphinxcontrib-towncrier
BuildRequires:	python3-towncrier >= 19.2
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

%prep
%setup -q -n sphinxcontrib-towncrier-%{version}

%{__sed} -i -e '/^get_scm_version/ s/=.*/= lambda **kwargs : "%{version}"/' docs/conf.py

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="xdist.plugin" \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif

%if %{with doc}
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
